# Active objective: beat the 71-point score

The user explicitly requested this persistent goal on 25 October 2026. Success
requires an official scored competition submission above the observed 71.48
reference, using eligible, reproducible offline code. Public development scores,
accepted uploads and successful tests do not prove success. The goal remains
active until official evidence meets it.

## Latest checkpoint: 26 October, 18:47 IST

User explicitly requested uploading the current best and checking results. The
official allowance read returned one remaining entry. Submitted the exact
completed original baseline version 2 as **57657435**. Its three source hashes
match the saved upload manifest. Kaggle accepted it and reported zero remaining
entries today. Official status rechecked at 18:47:07 IST: **PENDING**, scores
empty, no error.
Selection evidence: `reports/kaggle/best-candidate-submission.json`. Keep the goal
active; acceptance and the public development result do not prove >71.48.

Both controlled GPU experiments are now COMPLETE and analyzed. Original public
mean **43.7621**, 102 levels/five wins; rolling-summary **37.0547**, 89 levels/six
wins; Swift **11.3230**, 50 levels/zero wins. All 25 games in both variants have
verified model gameplay. Neither variant is promoted. These are single-pass
public comparisons, not estimates of hidden scores or causal proofs.

CPU repair v5 is officially ERROR. It passed headers and compiled the native
objects, then failed linking: `cannot find -lcudart`. Preserve its final log.
Version 6 is uploaded: it provides the unversioned cudart linker alias for the
versioned wheel library and adds a host link probe before the full native build.
Python compilation, Bash syntax and both runtime-overlay tests passed locally.
Cloud linker/build/offline checks remain unverified. Exact version and source
hashes are recorded in `reports/kaggle/pennyroyal-v3-repair-v6/upload.json`.
No v3 runtime has been promoted or GPU tested. The official submission uses the
validated original runtime and model.

Next: poll exact official submission **57657435**. It has a nine-hour evaluation
budget, with possible queue time. Previous best scored entry remains 0.02 until
the new official result is available. Do not submit again against today's limit.

## Earlier experiment checkpoints

Previous turn made progress by correcting audit classification and verified both
jobs live. This continuation found and launched a separate model experiment.

| Exact job | Last official status | Observer session |
|---|---|---|
| `kunalsinghh25/arc-hydra-duck-summary/1` | COMPLETE, public mean 37.0547 | ended |
| `kunalsinghh25/arc-hydra-pennyroyal-v3-dependency-repair/5` | ERROR, native linker missing cudart alias | ended |
| `kunalsinghh25/arc-hydra-duck-swift/1` | COMPLETE, public mean 11.3230 | ended |

Logs are `reports/kaggle/duck-summary-v1/live.log`,
`reports/kaggle/pennyroyal-v3-repair-v5/watcher.log`, and
`reports/kaggle/duck-swift-v1/live.log`. CPU log reconnect errors are observation
failures; authoritative status confirms the job is still running. Never restart
one of these versions just because startup or compilation takes time.
At approximately 18:24 UTC the CPU observer exhausted its reconnect attempts.
The exact cloud job was verified RUNNING and only the observer was reconnected
(new session 12606). Summary and Swift startup logs continue advancing within
their existing allowances; no new game result is available yet.

At approximately 18:34 UTC (26 October 00:04 IST), both GPU public readiness
checks passed. Their configured 7,200-second gameplay windows have begun.
Deadlines: Swift 26 October **02:02:58 IST**, summary **02:04:08 IST**. Structured
readiness evidence is in each run's `readiness.json`. Health and warmup resets
alone do not establish generated tokens, substantive actions or summary execution.
The earlier startup-only descriptions below are historical; retain both runs.

At approximately 18:38 UTC, substantive gameplay is verified in live printed
snapshots: Swift **two levels, 224 actions, 130,680 tokens**; summary variant
**three levels, 142 actions, 145,223 tokens**. Both snapshots are unfinished and
not synchronized comparisons; no memory benefit or model superiority is claimed.
Actual rolling-summary execution still needs verification after its interval.

CPU repair v4 is officially ERROR. Final log proves `nvrtc.h` was missing after
cuBLAS integration: the library filter excluded all `nvidia-cuda-*` packages,
including NVRTC. Repair v5 excludes only the specific compiler/runtime/CCCL
packages when extending the overlay; NVRTC and other CUDA libraries now remain
eligible. Added a compile probe including cuBLAS, NVRTC and CUDA standard headers
before the full native build. Python compilation and Bash syntax passed. V5
upload hashes and v4 final logs are retained; GPU experiments were not changed.
V5 was subsequently re-polled RUNNING; four targeted offline packaging tests pass.
Its first log observer (29593) later exhausted reconnect attempts and exited.
The exact v5 cloud job was re-polled RUNNING; only the observer was reconnected,
as session 39736. Both GPU gameplay runs continue on their original versions.
At approximately 19:15 UTC / 00:45 IST, v5 passed dependency checks and the
new cuBLAS/NVRTC/CCCL SM120f header-compilation probe. Structured stage evidence
is `reports/kaggle/pennyroyal-v3-repair-v5/header-probe.json`. This gets past the
two observed missing-header failures but does not prove native module completion,
fresh offline installation or GPU performance.

The CPU observer now uses `scripts/kaggle_watch.py`, session 17923, writing
`watcher.log` in UTF-16. Installed CLI source confirmed its default five quiet
reconnect failures caused repeated observer exits. The helper uses the same
deduplicating SDK stream with a longer retry allowance and reports authoritative
cloud status if it returns. It requires an exact version and never saves,
pushes, cancels or submits anything. The old observer may finish independently;
prefer `watcher.log` for subsequent CPU observations. Syntax/help checks passed.

Independent tool-API inspection found that component segmentation, rotation
hashes, adjacency and cross-frame movement already exist in the published
agent. Do not add a redundant component detector. Further perception changes
need concrete trace evidence and a separate controlled evaluation.

Swift 1.5 is a public reasoning-efficient derivative. An existing AutoRound INT4
mirror permits a target-only experiment with the original runtime/draft rather
than waiting for v3/NVFP4 integration. Same 25 games and 7,200-second gameplay
budget as the completed baseline; separate from the memory experiment. All 95
input files passed size checks, its 82-shard index is complete, and mounted
config SHA matches inspected upstream. No tensor data downloaded to Windows.
Research, pinned input inventory, notices and limitations: `baselines/swift_15`.
Local checks: **53 passed**. All three exact statuses above were read directly.

An auto-review rejection of a model-card read was resolved by inspecting the
CLI implementation: `model_get_cli` writes JSON metadata only; actual checkpoint
download is a separate method. The verified retry succeeded. No approval is
pending and no weights were transferred locally.

Completed baseline remains public **43.7621**, 102 levels/five wins. Official
hidden score remains **0.02**, with zero submissions remaining on the latest
official allowance read. Wait for live experiment results and the next allowance
before choosing a validated hidden-score candidate. Neither Swift nor the
summary/runtime experiments have established an improved score yet.

## Authoritative starting point

- v0.1: submission 57601062, COMPLETE, public score 0.01.
- v0.2: submission 57630597, COMPLETE, public score **0.02**, no evaluation error.
- v0.2 public development: 125 runs, five full FT09 wins, mean 3.9470. This is
  evidence of poor transfer, not a proxy for the objective.
- The live API leaderboard snapshot is `reports/kaggle/leaderboard-goal-start.json`.
  The observed leading entry is Yi-Chia Chen @ Fields Model, 71.48.
- One daily submission was used on 25 October. Query the official allowance
  before entering another candidate; private notebook validation is separate.

## Baseline experiment history (latest status is above)

Reproduce Daniel Franzen's public Milestone 2 model-based baseline, credited to
Franzen, Jeroen Cottaar and Tufa Labs. The author reports 27.89 for his submission;
this project has not reproduced that score. Code writes and executes Python to
investigate games; model weights and inference run locally on Kaggle.

- Version 1 is **COMPLETE**. Five-game public preflight verified real model
  gameplay: seven levels, zero full wins, subset mean score 11.397576782,
  119 actions and 135,986 accounted generated tokens. FT09 reached level 4;
  LS20, R11L and VC33 completed one level each; BP35 completed none.
- Source `serve.log` records 981.72 seconds of weight loading and roughly
  1,162 seconds of engine startup. The server became ready at 14:44:23 UTC;
  public gameplay ended at 14:50:45. Thus only about six minutes of model-ready
  play remained in the initial 900-second rollout. No serving crash was found.
- Artifacts: `reports/kaggle/duck-m2-preflight-v1`. Its raw summary incorrectly
  reads only terminal-turn tokens; the analyzer reconstructs action-plus-terminal
  tokens from `benchmark.json`, retaining the raw file and listing corrections.
  Cancellation notes can include additional uncharged generation. This is not
  an official hidden score, a full-set public mean or a matched v0.2 comparison.
- Version **2** is now the active job:
  `kunalsinghh25/arc-hydra-duck-m2-baseline/2`, official status RUNNING.
  All 25 public games, one pass, 7,200-second gameplay budget **after** model
  readiness. One-hour startup allowance; 12,000-second notebook timeout.
  Agent, model, serving, prompts and competition controls are unchanged.
- `notebooks/duck_m2` is the uploaded benchmark source; its file hashes are in
  `reports/kaggle/duck-m2-benchmark-v2/upload.json`. The alternate five-game
  repair at `notebooks/duck_m2_next` is prepared but not uploaded.
- 48 local tests pass, including public/competition separation, backend wait
  handling, the token-accounting regression and absolute contest deadline.
- `notebooks/duck_m2_candidate` is a **prepared, not uploaded** contest variant.
  Its only additional competition change sets the global soft deadline to the
  notebook's initial start + budget - 600 seconds, so startup is counted and
  finalization has ten minutes. The current version-2 benchmark remains the
  original competition behavior. Do not launch another version while it is live.
- Current live-log client session: **54334**, writing the ignored transient
  `reports/kaggle/duck-m2-benchmark-v2/live.log`. The previous observer 60229
  ended normally. An observer failure does not mean the Kaggle job stopped.
  Re-poll exact version 2; never restart it based only on elapsed startup time
  or absence of final artifacts.

## Independent work while version 2 runs

- Preflight request audit: 107 completed model responses, 143,977 completed-
  response tokens, three ordinary tool errors among 102 distinct visible tool
  results, and one expected stale-action guard stop. Per-game weighted cached
  prompt fractions range 0.8926–0.9391. `request-audit.json` preserves source-file
  hashes. Completed-response tokens differ from action-accounted tokens because
  some completed analysis made no action. Both omit unfinished generation.
- Decision: these data do not justify a broad syntax/tool rewrite. Preserve the
  agent baseline and use the longer run to inspect context loss and allocation.
- The primary public D-prime release explicitly reports large resubmission
  variance in the original: 27.62–31.47, versus one D-prime score of 31.54.
  Do not treat that single comparison as a verified causal improvement.
- Runtime v3 has no release wheel assets or ready maintained Kaggle bundle
  identified. It requires CUDA 13.3/GCC 15 and compiled accepted FlashInfer
  sources. A separate CPU-only online build is now running:
  `kunalsinghh25/arc-hydra-pennyroyal-v3-build/1`, 14,400-second cap.
  No models or competition data are attached. Source/pins are in
  `scripts/serving_v3`; upload hashes in `reports/kaggle/pennyroyal-v3-build-v1`.
- CPU build observer session **2793** writes that job's ignored `live.log`.
  Compiler probe passed, native Rust compilation started, no final build result
  yet. Require `BUILD_COMPLETE` plus offline checks, then real GPU inference and
  measured agent comparison. CPU build success alone is not a better agent.
- Latest quota snapshot: `reports/kaggle/accelerator-quota.json`, 4.1103 GPU
  hours used of 30, reserved 0, pay-to-scale disabled, refresh 31 October UTC.
  Recheck before allocating further substantial GPU work.
- Version-2 live snapshot at 15:54 UTC: 42 completed public levels, no full wins,
  all 25 games have actions, mean 11.32. It is explicitly **not final**. Its
  gameplay deadline is 17:18 UTC / 22:48 IST on 25 October.

The current continuation made progress: it produced the deduplicated request
audit, froze the v3 source/toolchain inputs, launched the independent CPU build,
and verified both exact remote jobs are still RUNNING. The GPU model experiment
has not finished; keep both job versions intact until authoritative terminal
states or output evidence justify the next action.

Read-only status/output commands:

```powershell
.venv/Scripts/python.exe scripts/kaggle_local.py kernels status kunalsinghh25/arc-hydra-duck-m2-baseline/2
.venv/Scripts/python.exe scripts/kaggle_local.py kernels output kunalsinghh25/arc-hydra-duck-m2-baseline/2 -p reports/kaggle/duck-m2-benchmark-v2
.venv/Scripts/python.exe scripts/analyze_duck_run.py reports/kaggle/duck-m2-benchmark-v2
```

## Next decisions from evidence

### Current state: 25 October, approximately 18:03 UTC

Follow-up at approximately 18:09 UTC: both exact jobs were re-polled and remain
RUNNING; no restart. Official submission-limits read confirms one used today,
two lifetime, **zero remaining today**. This is a verified wait on specific live
experiments, not a blocker requiring user input. Request audit corrected one
`TerminalStateActionError` to an expected guard stop: **23 ordinary errors,
seven stale-state stops, one terminal-state stop** in the six-file subset.
Two targeted profiler tests pass. Earlier 24-error counts below are historical.

- Previous turn made progress: repaired dependency packaging, preserved the
  native wheel and launched CPU repair version 3. It has now ended ERROR.
- GPU baseline version 2 is COMPLETE. Final public mean **43.76212092097825**,
  **102 levels, five full wins**, all 25 games with verified gameplay, no crashes.
  Full evidence and diagnostic interpretation: `reports/kaggle/duck-m2-benchmark-v2/findings.md`.
- Six weak-game request files audited: 395 completed responses, 808,231 tokens,
  24 ordinary tool errors, seven guard stops. BP35 generated 58,236 tokens over
  16 responses at one action counter, with large prompt reductions. This is a
  memory hypothesis, not proof that trimming caused failure or that thinking
  without actions is wasteful. No automatic stall cutoff was added.
- A matched public memory experiment is officially RUNNING:
  `kunalsinghh25/arc-hydra-duck-summary/1`. Same model/runtime, all 25 games,
  one pass, two-hour gameplay after readiness. Existing upstream rolling
  summaries enabled every 49,152 new context tokens, cap 4,096, current-turn
  context and summary-aware draining. Observer **98131** writes
  `reports/kaggle/duck-summary-v1/live.log`. Model serving has launched; readiness
  and actual summary execution are not yet established. Do not restart it.
- CPU repair v3 passed dependencies, then native FlashInfer compilation failed
  on missing `cublasLt.h`. Its final `v3-build.log` is retained. Repair **v4**
  adds Torch's already installed CUDA-library development files to the isolated
  compiler overlay while keeping compiler/runtime/CCCL 13.3. It is officially
  RUNNING: `kunalsinghh25/arc-hydra-pennyroyal-v3-dependency-repair/4`.
  Observer **72918**, `reports/kaggle/pennyroyal-v3-repair-v4/live.log`.
- Latest official quota read: 5.58/30 GPU hours used, 24.42 remaining. No billing
  changes. Official competition submission allowance still requires a fresh
  check after UTC date rollover; official score remains 0.02. The hidden-score
  baseline and score above 71.48 remain unverified.
- Local checks: **51 passed**, including experiment isolation and configuration
  export. The original baseline upload remains intact.

Next: preserve both exact live jobs. Require actual summaries before interpreting
the memory result. Require CPU compilation plus fresh offline checks before any
GPU runtime integration. Once official allowance returns, evaluate a validated
candidate on hidden games; public 43.76 does not establish that score.

### Update: 25 October, approximately 16:31 UTC

- Previous question turn produced new evidence: the live public benchmark had
  two full wins and mean 27.24. This is unfinished public evaluation, not hidden
  competition performance. A later snapshot reached 28.19; version 2 remains
  officially RUNNING and must finish on its existing 17:18 UTC gameplay deadline.
- CPU build version 1 is officially ERROR. Native wheel compilation succeeded,
  but the subsequent dependency check found five missing FlashInfer architecture
  providers. The retained final `v3-build.log` is authoritative. Missing wrapt in
  inherited sitecustomize was also observed. Both are addressed in the repair.
- Native-wheel ZIP integrity, exact version, native-extension presence and
  SHA-256 were checked before private dataset upload; provenance is in
  `reports/kaggle/pennyroyal-v3-build-v1/native-wheel.json`.
- Repair version 1 is officially ERROR: failed-job output was not a valid Kaggle
  kernel input. The uploader needs a native Windows absolute path on this host.
  The private retained-wheel dataset subsequently became ready; repair version 2
  accepted it but failed early wheel discovery. The dataset file listing proved
  Kaggle stripped `+` from the wheel filename. Version 3 handles that sanitized
  name, checks the original hash, then restores the correct wheel filename.
  Current ref: `kunalsinghh25/arc-hydra-pennyroyal-v3-dependency-repair/3`.
  CPU only, no models or competition input. Observer session 5080. Final overlay
  uploads must preserve filenames inside an archive rather than direct wheels.
  Version-3 live evidence confirms retained-wheel hash verification and the
  SM120f compiler probe passed. Official status is RUNNING as of 16:35 UTC;
  no final offline-check result yet. GPU version 2 is also officially RUNNING;
  latest observed unfinished public mean 30.21, still not a hidden score.
- Prepared offline GPU integration requires a completed bundle's real manifest
  hash and uses a distinct notebook ID. CPU artifact success, GPU inference,
  throughput improvement, agent improvement and hidden score remain unproven.
- Local checks: 50 tests passed; repaired Bash script syntax passed with Git Bash.
  The GPU baseline notebook files were not regenerated or replaced.

Next: observe the exact CPU repair and original GPU benchmark; inspect terminal
artifacts. Require CPU offline success before a separate GPU runtime test. The
runtime's native NVFP4 optimizations may not apply to the current INT4 model, so
do not assume a compatibility overlay provides its advertised speed gains.

1. Inspect terminal status, `serve.log`, `benchmark.json`, model transcripts and
   `hydra_model_summary.json`. Notebook completion alone is insufficient because
   the upstream benchmark can swallow solver errors; the derived run explicitly
   fails on crashed/not-started/no-action games.
   The analyzer additionally requires generated tokens and more than the warmup
   reset, because a reset alone does not prove model readiness.
2. Repair any proven packaging or inference failure without changing the agent
   until the original behavior is operational. Preserve each run/version.
3. Run all 25 public games with a meaningful model budget, retain failure types,
   generated-token costs, action efficiency and completion. Public evaluation is
   a development instrument, not an unseen-task estimate.
4. Reproduce an official hidden-score baseline when an allowance is available.
   Run the original nine-hour competition path; do not submit the public dummy.
5. Compare scheduling (including published D-prime), memory at context drains,
   model capability/throughput and tool feedback as separate interventions.
   Add Hydra symbolic helpers only if their measured benefit justifies it.
6. Continue improving until an official score above 71.48 is verified. Neither
   reproducing 27.89 nor beating our 0.02 baseline completes this objective.

Do not claim the leading team's current code is public or reproduced. Public
notebook titles and vote counts do not verify their leaderboard scores.
