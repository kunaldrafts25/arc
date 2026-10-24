# Experiment log

Date for all initial experiments: 2026-10-24 (Asia/Calcutta). Local public development results only. No leaderboard results or hidden evaluation claims.

## SETUP-01 — official baseline and Windows portability

- Agent version: unmodified starter at eeb1535.
- Hypothesis: the official local loop runs on this Windows Python 3.12 machine.
- Commands: `py -3.12 -m venv .venv`; pip install official dependencies; `python scripts/slim_framework.py`; `python -m pytest vendor/ARC-AGI-3-Agents/tests -q -p no:cacheprovider`; `python scripts/play_local.py --game ls20,vc33 --max-steps 50`.
- Failures: sandboxed ensurepip could not write temporary wheel files; approved environment setup succeeded. Original slim_framework wrote cp1252 Python source that could not import as UTF-8. First real ls20 run completed 51 commands and 0 levels, then terminal output failed on a Unicode arrow. Both Windows issues were corrected explicitly.
- Upstream suite after encoding fix: 4 collection errors (missing agents.structs and openai). Independent recorder suite: 19 passed.
- Decision: KEEP UTF-8 source writing and ASCII terminal status; preserve framework interfaces.

## BASE-01 — reproducible official starter smoke

- Commands: `python scripts/benchmark.py --bootstrap --policies starter --seeds 0 --steps 50 --games ls20,vc33 --output reports/starter-smoke.jsonl`; then all public games into reports/public-starter-smoke.jsonl.
- Baseline policy: pristine source loaded by git show; RNG reseeded deterministically after construction. Budget wrapper enforces equal exact caps, correcting the base loop's extra command.
- Evaluation: 25 advertised public games, policy seed 0, environment seed 0, 50 commands per game.
- Results: all 25 runs completed without exceptions. Detailed completions, action counts and scorecards in JSONL. This is a smoke check, not evidence of competitive play.
- Decision: KEEP as reproducible comparison.

## HYDRA-01 — legal actions, novelty, memory, empirical frontier planning

- Agent version: 0.1.0.
- Hypothesis: advertised action filtering and count-based exploration outperform the starter.
- Components: observation encoding, transition outcome counts, conservative repeated-edge predictions, bounded BFS, cycle recovery, per-instance RNG, validated click coordinates.
- Evaluation: ls20 and vc33; policy seeds 0,1,2; environment seed 0; 200 commands per game.
- Command: `python scripts/benchmark.py --policies starter,random,novelty,memory,planning --seeds 0,1,2 --steps 200 --output reports/ablation-v01.jsonl`.
- Baseline: 0 levels over 6 runs, mean local score 0.
- Legal random: 3 completed levels over 6 runs, mean local score 0.028675099667001106 on the 0–100 scale. All completions were vc33 level 1, once per seed; no full game wins.
- Novelty / memory / planning: each 1 completed level over 6 runs, mean local score 0.003682195009047679. These policies produced identical scores, so the extra model did not show a gain.
- Median runtime: starter 0.344 s; legal random 1.758 s; novelty 1.484 s; memory 1.640 s; planning 1.586 s. Component click candidate extraction adds CPU work.
- Exceptions: 0. ls20 remained unsolved. Very few repeated rendered states; no meaningful planning advantage demonstrated. Timers/animation/hidden state are candidate explanations, not a verified causal diagnosis.
- Decision: INVESTIGATE on the full public set; do not promote planning based on architecture alone.

## HYDRA-02 — full public ablation and temporally coherent experiments

- Hypothesis: holding simple actions for short sampled runs improves spatial exploration compared to changing action every step.
- Changed components: persistent policy holds IDs 1–4 for runs of length 2,4,8, stops after exact no-op, rechecks legality each step; never repeats coordinate clicks as an open-loop option.
- Evaluation: all 25 public games, policy seeds 0,1,2, environment seed 0, 200 commands. Six policies: starter, random, novelty, memory, planning, persistent.
- Command: `python scripts/benchmark.py --policies starter,random,novelty,memory,planning,persistent --seeds 0,1,2 --steps 200 --output reports/public-ablation-v01.jsonl`.
- Results and decision: recorded in reports/public-ablation.md after completion. No prospective result claimed here.

## HYDRA-03 — click coverage under changing rendered states

- Hypothesis: tracking tested click locations across frames reduces repeated uninformative probes when full-frame state keys change continually.
- Components: bounded level-local click counts, least-tested candidate bonus; active only in click-only states. Other states use memory exploration.
- Evaluation: all 25 public games, policy seeds 0,1,2, environment seed 0, 200 commands.
- Command: `python scripts/benchmark.py --policies coverage --seeds 0,1,2 --steps 200 --output reports/coverage-v01.jsonl`.
- Results and decision: recorded in reports/public-ablation.md after completion.

An early persistence run started while the game cache was still populating, was interrupted, and is excluded from comparisons (reports/persistence-v01.jsonl). Complete comparisons use the stable 25-game cache. Tests, bookkeeping, portability and failure isolation are retained for correctness independently of policy score.

## PROFILE-01 — identify CPU cost before optimizing

- Command: `python -m cProfile -o reports/profile-v01.prof scripts/benchmark.py --games vc33 --policies memory --seeds 0 --steps 200 --output reports/profile-run.jsonl`.
- Measured under profiling with other experiments running: agent loop 4.448 s; choose_action 4.076 s; connected-component extraction 3.858 s (197 calls).
- Interpretation: component extraction dominates policy CPU time in this click game. This is a measured runtime hotspot, not the main demonstrated scoring failure: total time is still below the local guard, while goal-directed completion is weak.
- Decision: INVESTIGATE vectorized/run-length labeling later if actual Kaggle runtime is binding. Do not add an unverified binary dependency merely to optimize local speed. Profile timings are not target GPU/runtime estimates.
