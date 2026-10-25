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

Job `kunalsinghh25/arc-hydra-pennyroyal-v3-build/1` ended ERROR after a successful
native wheel build. `pip check` found five architecture-provider requirements
missing from the FlashInfer cache umbrella installed with `--no-deps`.
Kaggle's inherited sitecustomize also reported missing wrapt. The repair resolves
the complete cache family and freezes wrapt into the runtime delta.

The native wheel was downloaded, checked for ZIP integrity, version and native
extensions, and SHA-256 verified:
`ffc0be8aa61168db6a521bb9eaae800e3cfde64d888170cc66fa9cde9dfa94a6`.
It is retained in our private dataset
`kunalsinghh25/arc-hydra-retained-v3-native-wheel`. This saves recompiling Rust;
the compiler probe, FlashInfer build and fresh offline checks still run.

```powershell
.venv/Scripts/python.exe scripts/build_serving_v3_notebook.py --reuse-wheel-sha256 ffc0be8aa61168db6a521bb9eaae800e3cfde64d888170cc66fa9cde9dfa94a6
.venv/Scripts/python.exe scripts/kaggle_local.py kernels push -p notebooks/serving_v3_repair --timeout 14400
```

The first repair version failed because Kaggle rejected the failed job as a
kernel input. Version 2 used the ready private dataset but failed its early input
check: Kaggle stripped `+` from the wheel filename. The dataset file listing
confirmed this. Version 3 accepts that sanitized filename, verifies the original
content hash and restores the valid wheel name before installation.
Version 3 passed `pip check`, then FlashInfer compilation failed on missing
`cublasLt.h`: the separate compiler environment omitted Torch's CUDA-library
development files. Version 4 extends the overlay with those installed libraries,
preserving the isolated CUDA compiler/runtime/CCCL 13.3 packages. The GPU
installer performs the same extension step after installing its runtime.
Version 4 is ERROR: the library-extension filter also excluded NVRTC, leaving
`nvrtc.h` unavailable. Version 5 excludes only the specific compiler packages,
allows NVRTC and other library packages, and compiles a cuBLAS/NVRTC/CCCL header
probe before the full FlashInfer build.
Current ref: `kunalsinghh25/arc-hydra-pennyroyal-v3-dependency-repair/5`.
Observer session 29593 writes `reports/kaggle/pennyroyal-v3-repair-v5/live.log`.
That observer subsequently expired; the exact cloud job remained RUNNING and
observer 39736 now follows it. V5 live evidence confirms dependency checks and
the cuBLAS/NVRTC/CCCL SM120f compilation probe passed. Full native compilation
and fresh offline verification are still pending; see `header-probe.json` in
the version-5 report directory.
The current CPU observer is session 17923 using `scripts/kaggle_watch.py`; its
preferred output is `reports/kaggle/pennyroyal-v3-repair-v5/watcher.log`. This
read-only helper extends the SDK's five-failure reconnect allowance for quiet
compilation, deduplicates replayed events through the SDK, and reports cloud
status when observation ends. It never restarts the job.

```powershell
.venv/Scripts/python.exe scripts/kaggle_watch.py kunalsinghh25/arc-hydra-pennyroyal-v3-dependency-repair/5 --output reports/kaggle/pennyroyal-v3-repair-v5/watcher.log
```
Preserve original wheel paths in an archive when packaging the final overlay;
direct wheel uploads can alter filenames while leaving their contents unchanged.

`install_overlay.py` and the optional runtime-overlay arguments of
`build_duck_notebook.py` prepare a separate offline GPU candidate. They require
the actual completed bundle manifest hash; no v3 GPU candidate has been launched.
