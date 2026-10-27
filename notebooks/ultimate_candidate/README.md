# ARC-Hydra Ultimate Candidate

This is an experimental candidate, not a demonstrated best-scoring submission.
It uses the original Intel AutoRound Qwen3.8-Flash-Next checkpoint and draft,
the operational v2.5.3 serving stack, mechanically checked planning, corrected
system/user prompts, backend readiness checks, lifecycle records and a ten-minute
competition finalization reserve. Model weights are frozen.

The builder checks source hashes against completed offline CPU probe **v4**,
which passed seven sandbox cases and 16 rendered user-prompt combinations.
This validates integration, not GPU inference, gameplay gains or hidden scores.
Original attribution and license notices remain in the notebook.

Build and run the bounded pilot:

```powershell
.venv/Scripts/python.exe scripts/build_ultimate_notebook.py --mode preflight
.venv/Scripts/python.exe scripts/kaggle_local.py kernels push -p notebooks/ultimate_candidate --timeout 3600
```

The pilot uses five public games for 900 seconds after backend readiness.
The one-hour cap covers startup, gameplay and output finalization. Private,
internet-disabled, RTX PRO 6000, no official submission and no paid scaling.

After verifying gameplay, errors and actual helper use, a separate full benchmark
can be built with `--mode benchmark` (25 public games, 7200 seconds after
readiness). Rebuilds must preserve exact uploaded-version provenance. Official
competition reruns use the competition time controls and global finalization
reserve. Do not submit based on the five-game pilot alone.

The preceding strict-planner run is a separate configuration with older user
guidance. It was trailing the baseline in unfinished public snapshots. Neither
its final outcome nor the benefit of this correction was established when this
candidate was packaged. Retain the official best submission until stronger
evidence justifies promotion. Goal: official 100, or beat the latest verified
competing leader; public practice scores cannot establish completion.
