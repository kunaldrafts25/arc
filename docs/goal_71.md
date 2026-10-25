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

- Job: `kunalsinghh25/arc-hydra-duck-m2-baseline`, version 1.
- Uploaded with RTX PRO 6000, internet disabled, 3,600-second notebook timeout.
- Official status confirmed RUNNING after upload and again during source audit.
- Output download currently returns no artifacts. Model readiness and actual
  gameplay are unproven. Re-poll this same job; do not restart from a timeout or
  absent interim output alone.
- Public preflight: FT09, LS20, R11L, VC33, BP35, one pass, 900-second gameplay
  deadline after initialization. This is a runtime/gameplay check, not a matched
  full-score reproduction. Original competition controls are retained.
- `scripts/build_duck_notebook.py` builds the attributed notebook; its source,
  model mounts, container image and SHA provenance are preserved. 41 local tests
  pass, including checks that the preflight does not alter contest controls.

Read-only status/output commands:

```powershell
.venv/Scripts/python.exe scripts/kaggle_local.py kernels status kunalsinghh25/arc-hydra-duck-m2-baseline
.venv/Scripts/python.exe scripts/kaggle_local.py kernels output kunalsinghh25/arc-hydra-duck-m2-baseline -p reports/kaggle/duck-m2-preflight-v1
.venv/Scripts/python.exe scripts/analyze_duck_run.py reports/kaggle/duck-m2-preflight-v1
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
