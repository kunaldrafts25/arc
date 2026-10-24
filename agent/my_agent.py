"""ARC-Hydra v0.1; official Agent adapter, no game-specific rules."""
from __future__ import annotations
from hashlib import blake2b
import threading
import time
import logging
from arcengine import FrameData, GameAction, GameState
from agents.agent import Agent
from hydra.controller import Controller
from hydra.perception import normalize, state_key, components, grid_diff


_ACTION_LOCK = threading.RLock()


def legal_candidates(observation, rng, object_clicks=True):
    legal = []
    for value in getattr(observation, "available_actions", []) or []:
        try:
            action = GameAction.from_id(value)
        except ValueError:
            continue
        if action is not GameAction.RESET:
            legal.append(action)
    candidates = [(a.value, None, None) for a in legal if a.is_simple()]
    if GameAction.ACTION6 in legal:
        frames = normalize(observation)
        points = []
        if frames and object_clicks:
            grid = frames[-1]
            if grid.size <= 4096:
                points = [obj["point"] for obj in components(grid) if obj["area"] < grid.size / 2][:64]
        points += [(x, y) for y in (8, 24, 40, 56) for x in (8, 24, 40, 56)]
        points += [(rng.randrange(64), rng.randrange(64))]
        candidates += [(6, x, y) for x, y in dict.fromkeys(points) if 0 <= x < 64 and 0 <= y < 64]
    return candidates


def validate_action(choice, observation):
    action_id, x, y = choice
    if action_id != 0 and action_id not in (getattr(observation, "available_actions", []) or []):
        raise ValueError("Action not advertised by the current observation")
    action = GameAction.from_id(action_id)
    payload = {"game_id": getattr(observation, "game_id", "")}
    if action.is_complex():
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Complex action requires integer coordinates")
        payload.update(x=x, y=y)
    action.validate_data(payload)
    return action, payload


class MyAgent(Agent):
    MAX_ACTIONS = 200
    MAX_SECONDS = 600.0
    POLICY = "novelty"
    OBJECT_CLICKS = True

    def __init__(self, *args, **kwargs):
        seed = kwargs.pop("hydra_seed", 0)
        policy = kwargs.pop("hydra_policy", self.POLICY)
        super().__init__(*args, **kwargs)
        self.action_counter = 0
        game_seed = int.from_bytes(blake2b(self.game_id.encode(), digest_size=8).digest(), "big")
        self.controller = Controller(seed ^ game_seed, policy)
        self.started = time.monotonic()
        self.level = None
        self.previous_grid = None
        self.last_diff = None
        self.observation_history = []
        self.errors = []
        self._payload = {}
        self._reasoning = {}

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return (latest_frame.state == GameState.WIN
                or self.action_counter >= self.MAX_ACTIONS
                or time.monotonic() - self.started >= self.MAX_SECONDS)

    def main(self):
        # Swarm constructs every game before starting any agent thread. Exclude
        # that setup wait from this instance's decision-time allowance.
        self.started = time.monotonic()
        try:
            super().main()
        except Exception as error:
            self.errors.append(f"{type(error).__name__}: {error}")
            logging.exception("Hydra stopped game %s after an environment/agent failure", self.game_id)
            self.cleanup()

    def choose_action(self, frames: list[FrameData], latest_frame: FrameData) -> GameAction:
        state = getattr(latest_frame, "state", GameState.NOT_PLAYED)
        level = getattr(latest_frame, "levels_completed", 0)
        reset = state in (GameState.NOT_PLAYED, GameState.GAME_OVER)
        if reset or level != self.level or getattr(latest_frame, "full_reset", False):
            self.controller.reset_level()
            self.previous_grid = None
            self.level = level
        if reset:
            choice = (0, None, None)
            self.controller.stats["resets"] += 1
        else:
            try:
                rendered = normalize(latest_frame)
                if rendered:
                    grid = rendered[-1]
                    self.last_diff = grid_diff(self.previous_grid, grid) if self.previous_grid is not None else None
                    self.previous_grid = grid
                self.observation_history.append(rendered)
                self.observation_history = self.observation_history[-8:]
                key = state_key(latest_frame)
                self.controller.observe(key)
                candidates = legal_candidates(latest_frame, self.controller.rng, self.OBJECT_CLICKS)
                choice = self.controller.choose(key, candidates) if candidates else (0, None, None)
            except (ValueError, TypeError, OverflowError) as error:
                self.errors.append(f"{type(error).__name__}: {error}")
                self.controller.reset_level()
                choice = (0, None, None)
        action, self._payload = validate_action(choice, latest_frame)
        self._reasoning = {"policy": self.controller.policy, "mode": self.controller.mode}
        with _ACTION_LOCK:
            action.set_data(self._payload)
            action.reasoning = self._reasoning
        return action

    def do_action_request(self, action: GameAction) -> FrameData:
        # Pass per-agent snapshots directly: the attached framework reads mutable
        # enum payloads, and a lock around its HTTP request serializes every game.
        raw = self.arc_env.step(action, data=self._payload.copy(), reasoning=self._reasoning.copy())
        return self._convert_raw_frame_data(raw)
