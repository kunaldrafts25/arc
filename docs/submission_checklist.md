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
- Target Kaggle wheel versions, GPU/RAM/time budget, rules acceptance and hidden rerun: NOT VERIFIED.
- Kaggle username: kunalsinghh25; private notebook ID kunalsinghh25/arc-hydra-arc-agi-3.
- Project-local Kaggle token: absent at initial inspection. Never paste tokens into chat or commit them.

## Remote workflow

1. Authenticate Kaggle locally and accept the competition rules through Kaggle. Confirm external data/model permissions, runtime, action limits and actual deadline against the authenticated rules. The webpage was not readable through the research tool.
2. Keep the competition attachment and internet disabled in notebooks/kernel-metadata.json. No external model weights are needed.
3. Build the notebook again after every agent/source change.
4. Use the official `make submit` on a POSIX environment, or install the Kaggle CLI in the project venv and use `kaggle kernels push -p notebooks` on Windows with local authentication configured. The original Makefile expects .kaggle/access_token and exports it as KAGGLE_API_TOKEN; do not print its content.
5. Track `kaggle kernels status kunalsinghh25/arc-hydra-arc-agi-3`. Save/run success checks commit execution; it does not execute the hidden game loop.
6. Inspect output, then select **Submit to Competition** and **submission.parquet** through Kaggle. Do not submit a hand-written score file. The gateway produces actual gameplay results during rerun.
7. Verify the competition rerun finishes and record its actual leaderboard result, runtime and logs before describing this as a validated competition submission.

No remote notebook or competition submission has been claimed by this checklist. Notebook building preserves the official gateway workflow and packages every Hydra Python module; source validation is a useful intermediate check, not target-environment validation.

Final default: novelty action-count exploration with bounded raw transition tracking. Predictive-model and BFS variants remain optional benchmark policies because they did not improve the measured score. Rebuild published comparisons with `python scripts/consolidate_experiments.py`; this excludes the superseded novelty ablation and verifies game/seed coverage before producing reports.
