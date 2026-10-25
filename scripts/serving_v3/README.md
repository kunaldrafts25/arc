# Pennyroyal v3 runtime experiment

This is an isolated CPU build, not a validated replacement for the model agent.
The running public baseline retains its original v2.5.3 runtime.

Upstream release: `pennyroyal-v3.0.0`, commit
`560edbdca18aedae13f71ae20b3984efa4d22633` in
https://github.com/jpezzulli/sglang-rtxpro6000.
The build follows its `BUILD.md` and accepted FlashInfer packaging installer.
CUDA 13.3 packages and the micromamba binary/hash are frozen in `pins.json`.
Compiler package URLs are frozen after resolution in `compiler-explicit.txt`.

The experiment builds on Daniel Franzen's public offline wheelhouse. It carries
his inspected INT4 scale-dtype fix and adapts his CUDA wheel-overlay assembly
(Apache-2.0; see `baselines/duck_m2/LICENSE`). Other runtime changes come from the
pinned upstream release. It does not change the model, prompts or agent policy.

```powershell
.venv/Scripts/python.exe scripts/build_serving_v3_notebook.py
.venv/Scripts/python.exe scripts/kaggle_local.py kernels push -p notebooks/serving_v3_build --timeout 14400
```

The generated notebook is private, configured for CPU, with internet enabled
for building and no competition or model attachment. Its output is an offline
delta against `dfranzen/pennyroyal-v253`, not a standalone full distribution.
Do not submit the build notebook to the competition.

The build must pass:

1. SHA verification of micromamba and exact upstream Git commit verification.
2. A CPU-side CUDA SM120f compilation probe with the new toolchain.
3. SGLang native-extension build and accepted FlashInfer source/kernel packaging.
4. Version-frozen delta wheel materialization and a fresh offline reinstall.
5. Dependency checks and upstream accepted-source/kernel verification.

Only then is `BUILD_COMPLETE` written. CPU build success does **not** establish
GPU loading, inference correctness, throughput improvement, model quality or
competition eligibility/performance. Preserve third-party notices and inspect
the resulting artifact manifest before any runtime integration.

The next stage, if the build succeeds, is to prepare an offline overlay installer
for a separate GPU candidate, verify model loading/inference, and run a matched
agent comparison. The current baseline must finish before being replaced.

Job `kunalsinghh25/arc-hydra-pennyroyal-v3-build/1` is running. Its live log has
confirmed the compiler probe passed and native Rust compilation began. Final
build and offline-install results are still unknown.
