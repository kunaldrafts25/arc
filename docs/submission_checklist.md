# Deployment and submission checklist

## Local commands (PowerShell from repository root)

```powershell
./scripts/setup_windows.ps1
.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
.venv/Scripts/python.exe scripts/benchmark.py --bootstrap --policies novelty --seeds 0 --steps 200
# After the first public game cache download, omit --bootstrap for offline runs.
.venv/Scripts/python.exe scripts/play_local.py --offline --game ls20,vc33 --max-steps 50
.venv/Scripts/python.exe scripts/build_notebook.py
.venv/Scripts/python.exe scripts/verify_notebook.py
```

The local .venv, vendor framework and game cache exist in this workspace. For another Windows machine, setup_windows.ps1 reproduces the lightweight setup. Resolved versions are in requirements-lock.txt. `--Offline` setup needs a prepopulated wheelhouse; the final Kaggle notebook uses the competition's wheel dataset instead.

For diagnosis, add `--record` to benchmark.py. The official recorder saves raw frame/action evidence under recordings/ (gitignored), and the result row records its filename. Results without this flag retain metrics and scorecards, while complete image histories exist only during the run.

## Current validation boundary

- Actual official engine public gameplay: executed.
- Unit tests, lifecycle and payload validation: executed.
- Notebook source extraction/import outside source tree: executed.
- Authenticated rules/file access, nine-hour runtime, offline restriction and attached wheel versions: verified; hardware RAM and hidden rerun remain unverified.
- Kaggle username: kunalsinghh25; private notebook ID kunalsinghh25/arc-hydra-arc-agi-3.
- Project-local Kaggle token: configured and validated after initial inspection. Authentication is handled by scripts/kaggle_local.py.
- Notebook version 2: COMPLETE; public smoke passed in the actual Kaggle environment, 20 actions per game and no exceptions.
- Competition submission: accepted as 57601062; read reports/kaggle/submission-status.json for scoring status. Daily allowance is now zero.

## Remote workflow

1. Authentication and competition entry are confirmed. The authenticated SDK pages supplied rules and runtime/deadline requirements; per-game action limits and hardware RAM remain unverified.
2. Keep the competition attachment and internet disabled in notebooks/kernel-metadata.json. No external model weights are needed.
3. Build the notebook again after every agent/source change.
4. Use `.venv/Scripts/python.exe scripts/kaggle_local.py kernels push -p notebooks --accelerator NvidiaTeslaT4 --timeout 32400` on Windows. The wrapper reads .kaggle/access_token internally. Only one competition submission per day is allowed; notebook Save/Run is a separate validation stage.
5. Track `kaggle kernels status kunalsinghh25/arc-hydra-arc-agi-3`. Save/run success checks commit execution; it does not execute the hidden game loop.
6. Inspect output, then select **Submit to Competition** and **submission.parquet** through Kaggle. Do not submit a hand-written score file. The gateway produces actual gameplay results during rerun.
7. Verify the competition rerun finishes and record its actual leaderboard result, runtime and logs before describing this as a validated competition submission.

See docs/kaggle_validation.md for remote notebook and competition status. The notebook preserves the official gateway workflow, packages every Hydra module and now runs an offline public-game smoke test during commit mode. Successful commit mode does not establish a hidden competition score.

Final default: novelty action-count exploration with bounded raw transition tracking. Predictive-model and BFS variants remain optional benchmark policies because they did not improve the measured score. Rebuild published comparisons with `python scripts/consolidate_experiments.py`; this excludes the superseded novelty ablation and verifies game/seed coverage before producing reports.
