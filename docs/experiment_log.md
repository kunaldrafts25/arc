# Experiment log

Erratum: the initial policy named novelty still consulted transition predictions, so its original rows are not a clean model-disabled ablation. They remain preserved in the raw logs. The corrected policy forbids model training and prediction while retaining raw transition evidence. Final comparisons replace the affected novelty rows with reports/novelty-corrected-v01.jsonl. A regression test enforces the boundary. The original six-policy run produced 450 rows with no per-run exceptions; memory and planning had zero model predictions and zero planned actions.

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
- Results: 75 runs per policy. Starter mean 0.061294 (3 level completions); random/persistent each 0.075703 (6); memory/planning each 0.149726 (4), on the 0–100 scale. No full wins. Legacy novelty rows are superseded as described in the erratum.
- Decision: no measured benefit from persistence or planning. Do not promote them to the production default. Preserve optional variants for reproducibility.

## HYDRA-03 — click coverage under changing rendered states

- Hypothesis: tracking tested click locations across frames reduces repeated uninformative probes when full-frame state keys change continually.
- Components: bounded level-local click counts, least-tested candidate bonus; active only in click-only states. Other states use memory exploration.
- Evaluation: all 25 public games, policy seeds 0,1,2, environment seed 0, 200 commands.
- Command: `python scripts/benchmark.py --policies coverage --seeds 0,1,2 --steps 200 --output reports/coverage-v01.jsonl`.
- Results: 75 runs, 3 level completions, 0 full wins, mean local score 0.008066. All completions were r11l level 1. Zero recorded exceptions.
- Decision: REVERT as a default candidate; cross-frame click suppression did not improve the measured objective. Retain only as an experimental policy.

## HYDRA-04 — ablation correction and seed confirmation

- Hypothesis: separating the novelty action-count policy from the transition model gives an interpretable ablation; additional policy seeds test whether the apparent gain repeats.
- Correction: novelty neither trains outcome distributions nor consults their predictions. Bounded raw transition tuples are still retained for debugging.
- Commands: `python scripts/benchmark.py --policies novelty --seeds 0,1,2,3,4 --steps 200 --output reports/novelty-corrected-v01.jsonl`; `python scripts/benchmark.py --policies memory --seeds 3,4 --steps 200 --output reports/memory-confirmation-v01.jsonl`.
- Baseline/random confirmation: seeds 3,4 in reports/confirmation-v01.jsonl; its legacy novelty rows are superseded and excluded from the final report.
- Evaluation: the same 25 public games, fixed environment seed 0. These are additional policy seeds, not held-out games and not evidence of hidden-set generalization.
- Results: corrected novelty and memory each averaged 0.1491665471 over 125 runs (25 games × 5 seeds), with 9 level completions and 0 full wins. Starter averaged 0.0374617995 with 4 completions; legal random averaged 0.0584301651 with 9. On separate seeds 3,4, novelty/memory averaged 0.148328; starter 0.001714; random 0.032521. All scores are on the 0–100 scale.
- Decision: KEEP corrected novelty as the simpler default. Transition prediction/planning remain experimental because neither improved its result. Final consolidated reports contain 525 training rows and 200 confirmation rows, all complete and without recorded exceptions. Additional policy seeds are not held-out games.

## FINAL-01 — production default and notebook verification

- Selected policy: corrected novelty with bounded raw transition tracking and legal action validation.
- Command: `python scripts/play_local.py --offline --game ls20,vc33 --max-steps 50`.
- Result: ls20 0 completed levels / 50 commands; vc33 1 completed level / 50 commands; aggregate local scorecard 0.08034894398530763. This short-ID smoke run uses the helper's normal game identifiers and is separate from full-ID seeded benchmark comparisons.
- Tests: `python -m pytest -q` → 19 passed. An earlier final check exposed that the model-reset test implicitly relied on the old default; it now explicitly selects the memory policy it tests.
- Packaging: `python scripts/build_notebook.py` and `python scripts/verify_notebook.py` succeeded. Bundled source imported and emitted a validated ACTION6 in a fresh isolated interpreter. `pip check` found no broken dependencies.
- Boundary: no Kaggle token was present. No remote notebook execution, hidden competition rerun or successful competition submission has been asserted.

## KAGGLE-01 — authenticated deployment

- The user configured a new project-local token. Authentication and prior competition entry were confirmed without displaying credentials.
- Verified official pages: nine-hour runtime, disabled internet, one submission/day, 110 private games, final deadline November 2 at 23:59 UTC. Attached arc-agi 0.9.8 / arcengine 0.9.3 interfaces and scorer were inspected.
- Deployment fix: send per-agent payload copies directly to the verified wrapper so concurrent games are not serialized by a shared HTTP lock. Extend the per-game wall guard to 600 seconds; action cap stays 200. No policy-score gain is claimed from these changes.
- Kaggle notebook v1: COMPLETE with expected commit-mode parquet.
- Kaggle notebook v2: COMPLETE; actual offline public smoke ran 20 actions each on ls20/vc33, no exceptions. The smoke cell is skipped during competition rerun. Full local suite: 21 passed.
- Submitted notebook v2 as competition submission 57601062. Kaggle accepted it, leaving zero daily submissions. Initial scoring status PENDING, with no score yet. Live status is recorded in reports/kaggle/submission-status.json.
- Decision: KEEP as the first validated deployment baseline; evaluate the actual competition result before claiming hidden-set performance.

## KAGGLE-RESULT-01 — first scored submission

- Submission: 57601062, notebook version 2.
- Official API result: COMPLETE; public score 0.01; private score unavailable; evaluation error empty.
- Own-submission download: HTTP 403. Per-game metrics remain unavailable; no alternative access path was attempted.
- Interpretation: valid scored baseline with weak performance; do not infer hidden completion/action counts or assign a specific failure cause from this aggregate alone.

## BUDGET-01 — test the 200-action guard

- Hypothesis: the small development cap substantially limits completion.
- Components changed: benchmark cap only, 200 versus 1,000 commands; same novelty policy and official loop.
- Games: cd82, ls20, r11l, vc33; policy seeds 0,1,2; environment seed 0.
- Baseline: 12 runs, 2,400 commands, 4 completed levels, 0 full wins, mean local score 0.9357866260, median runtime 1.812 s.
- Candidate: 12 runs, 12,000 commands, 6 completed levels, 0 full wins, mean local score 0.9359760621, median runtime 7.1015 s.
- Exceptions: 0. Failures: cd82 and ls20 remain unsolved; r11l stops at one completed level; two additional vc33 first-level completions are highly inefficient.
- Decision: INVESTIGATE mechanics/goal inference next; do not promote the fivefold cap globally from this small gain on four games.
- Independent guard fix: start the per-game timer when main begins, excluding Swarm construction waits. Local behavioral test verifies play still occurs after a simulated long setup wait. 22 tests pass. No hidden-score benefit is claimed; this source change has not been submitted.

An early persistence run started while the game cache was still populating, was interrupted, and is excluded from comparisons (reports/persistence-v01.jsonl). Complete comparisons use the stable 25-game cache. Tests, bookkeeping, portability and failure isolation are retained for correctness independently of policy score.

## PROFILE-01 — identify CPU cost before optimizing

- Command: `python -m cProfile -o reports/profile-v01.prof scripts/benchmark.py --games vc33 --policies memory --seeds 0 --steps 200 --output reports/profile-run.jsonl`.
- Measured under profiling with other experiments running: agent loop 4.448 s; choose_action 4.076 s; connected-component extraction 3.858 s (197 calls).
- Interpretation: component extraction dominates policy CPU time in this click game. This is a measured runtime hotspot, not the main demonstrated scoring failure: total time is still below the local guard, while goal-directed completion is weak.
- Decision: INVESTIGATE vectorized/run-length labeling later if actual Kaggle runtime is binding. Do not add an unverified binary dependency merely to optimize local speed. Profile timings are not target GPU/runtime estimates.

## MECHANICS-02 — learned mechanics and visual goals, 25 October 2026

- Hypothesis: intervention-based motion/tile models and example-based visual
  goals will outperform state novelty when action effects are regular.
- Changes: meter abstraction, inferred displacement controls, binary XOR and
  prime-cycle models, observed glyph equality/inequality programs, partial-panel
  constraints, marked-tile recognition and prediction checks. No game-ID policy.
- Evidence: `reports/v02` raw local scorecards and source snapshots. Intermediate
  experiments and failure diagnoses are described in `docs/v02_development.md`.
- Matched comparison: all 25 public games, environment seed 0, policy seeds
  0–2, strict 300-action cap, 75 runs each. Novelty mean 0.150198925, six level
  completions, no full wins. Candidate mean 3.942818150, 27 level completions,
  three full wins. Neither recorded exceptions.
- Concentration: all full wins are FT09. The candidate regresses on some games;
  gains do not establish a generally capable solver or unseen-task accuracy.
- Additional policy seeds 3 and 4 are evaluated separately. They change policy
  randomness, not game layout, and do not constitute unseen tasks.
- Additional-seed result: 50 runs, mean 3.953284272, 17 completed levels, two
  full wins, no exceptions. All 125 candidate runs: mean 3.947004599,
  44 completed levels, five full wins, no exceptions. Coverage/source digests
  validated by `scripts/report_v02.py --require-complete`; per-game summary in
  `reports/v02/comparison.json`.
- Local validation: 38 tests pass; extracted notebook source imports and chooses
  a legal complex action in an isolated interpreter.
- Target validation: private Kaggle version 3 COMPLETE; six FT09 levels and WIN
  in 159 actions, plus LS20/VC33 smoke actions, no exceptions.
- Decision: PROMOTE v0.2 reasoning/300 as the measured candidate; retain novelty
  for comparisons. Submitted as 57630597, initially PENDING, no evaluation error.
  This used the available daily attempt. Hidden results must come from the
  official status API, independently of these public measurements.
