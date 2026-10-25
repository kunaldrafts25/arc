# Active objective: beat the 71-point score

The user explicitly requested this persistent goal on 25 October 2026. Success
requires an official scored competition submission above the observed 71.48
reference, using eligible, reproducible offline code. Public development scores,
accepted uploads and successful tests do not prove success. The goal remains
active until official evidence meets it.

## Authoritative starting point

- v0.1: submission 57601062, COMPLETE, public score 0.01.
- v0.2: submission 57630597, COMPLETE, public score **0.02**, no evaluation error.
- v0.2 public development: 125 runs, five full FT09 wins, mean 3.9470. This is
  evidence of poor transfer, not a proxy for the objective.
- The live API leaderboard snapshot is `reports/kaggle/leaderboard-goal-start.json`.
  The observed leading entry is Yi-Chia Chen @ Fields Model, 71.48.
- One daily submission was used on 25 October. Query the official allowance
  before entering another candidate; private notebook validation is separate.

## Current experiment

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
- 46 local tests pass, including public/competition separation, backend wait
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

Read-only status/output commands:

```powershell
.venv/Scripts/python.exe scripts/kaggle_local.py kernels status kunalsinghh25/arc-hydra-duck-m2-baseline/2
.venv/Scripts/python.exe scripts/kaggle_local.py kernels output kunalsinghh25/arc-hydra-duck-m2-baseline/2 -p reports/kaggle/duck-m2-benchmark-v2
.venv/Scripts/python.exe scripts/analyze_duck_run.py reports/kaggle/duck-m2-benchmark-v2
```

## Next decisions from evidence

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
