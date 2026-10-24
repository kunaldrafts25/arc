# Competition specification — verified 2026-10-24

This is a development audit, not certification of eligibility or submission validity.

| Requirement | Finding | Source / status |
|---|---|---|
| Rules, external data, pretrained models | UNVERIFIED: Kaggle rules returned no readable content | https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3/rules |
| Runtime, RAM, action budgets | UNVERIFIED; do not confuse the starter's 80-action cap with competition limits | Kaggle overview inaccessible |
| Deadline | November 2, 2026 supplied by developer; official deadline UNVERIFIED | User request; Kaggle timeline inaccessible |
| Python | Starter requires 3.12 | Official starter README and Makefile |
| GPU | Starter supports CPU, T4, P100, RTX6000; defaults T4 | README and scripts/build_notebook.py; actual allocation UNVERIFIED |
| Internet | Generated notebook disables internet; installs from attached wheels | scripts/build_notebook.py, notebooks/kernel-metadata.json |
| Submission | Starter builds a notebook; gateway produces submission.parquet during competition rerun | scripts/build_notebook.py |
| Save/run versus evaluation | Save/run emits dummy parquet; hidden competition rerun executes agent | scripts/build_notebook.py; passing save/run alone does not validate gameplay |
| Upload | make submit builds and pushes; competition entry is a separate Kaggle UI step | README / Makefile |
| Public versus hidden | Local development games are not the hidden evaluation set | README |
| Memory boundaries | Agent object per game; no cross-game memory planned | vendor framework agents/swarm.py |
| Optional models | No weights or hosted inference used in v0.1 | Implementation decision; permissions remain unverified |

Official starter: https://github.com/arcprize/ARC-AGI-3-Kaggle-Starter

Scoring documentation: https://docs.arcprize.org/methodology

RHAE combines completion and squared human/agent action ratios. Documentation specifies a per-level 1.15 cap, level-index weights, a completion-dependent game cap, and averaging across games. Local engine implementation must be checked before implementing an independent estimate. Missing human baselines must remain unavailable. Counts from the agent loop may differ from scorecard counts, particularly for resets. There is no evidence here authorizing action batching or establishing reset cost. Read the installed wrapper and scorecard before relying on either.

Before any final submission: read the authenticated competition rules, confirm exact hardware/runtime/data restrictions and deadline, attach the competition data, configure the Kaggle handle, and execute the notebook in Kaggle. None of those checks is implied by a locally generated notebook.

## Installed implementation verification

Installed arc-agi 0.9.9 / arcengine 0.9.3, under Python 3.12.10. Exact transitive versions are in requirements-lock.txt; these are local versions, not verified Kaggle wheel versions.

- `arcengine/enums.py`: FrameData.frame is list[list[list[int]]], with state, levels_completed, win_levels, action_input, guid, full_reset and available_actions. FrameDataRaw.frame is a runtime list of NumPy arrays. Policy input is observed images and advertised actions only.
- GameAction IDs: RESET 0; ACTION1 through ACTION7 are 1 through 7. Only ACTION6 is ComplexAction, with x/y integers in 0..63. SimpleAction has optional game_id. The adapter does not assume game-specific action semantics.
- `arc_agi/wrapper.py`: reading observation_space returns the last response, without submitting an action. action_space converts advertised IDs. No action batching exists in the inspected interface.
- `arcengine/base_game.py`: RESET restarts the current level after play; it performs a full reset at action count 0 or after WIN, subject to ONLY_RESET_LEVELS. GAME_OVER is recovered through RESET.
- `arc_agi/scorecard.py`: initial full reset opens a play without charging a reset action; level reset increments reset and action counts. IDs 1 through 7 increment scorecard actions. The harness preserves raw official scorecards alongside agent command counts.
- EnvironmentScoreCalculator uses min(115, 100*(human/actions)**2) for completed levels with positive action counts, otherwise zero. It weights by 1-indexed level and caps the result by completed positive-score weights / all level weights times 100. The scorecard averages games. Missing baselines produce zero plus a diagnostic message in the package; our harness instead reports those scores as unavailable.

Metric calculation delegates to the installed official scorer. Tests cover weighting, completion cap, efficiency and unavailable baselines. Hidden gateway compatibility still requires a Kaggle run.
