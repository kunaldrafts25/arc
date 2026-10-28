# ARC-AGI-2 starting track

Authorized separately by the user on 29 October 2026 IST. This track does not
replace the active ARC-AGI-3 objective or share its score records.

## Verified competition state

Original account kunalsinghh25 is entered in ARC-AGI-2. The official format is
`submission.json`, with two named attempts for every test output of every input
task. Scoring averages exact matches over test outputs, not over tasks. Current
leader observed at setup: Tufa Labs, 88.06. The final deadline is 2 November
23:59 UTC / 3 November 05:29 IST. Runtime limit is 12 hours, offline execution.
See the [official competition](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/).

## Starting floor and official result

`arc2/symbolic.py` searches a bounded, task-local family of geometry, color-map,
crop, object, scale, tile and split-grid transformations. Candidates must match
the task's demonstration outputs; task IDs and test target labels are not used.
Distinct predictions are retained, with an explicit copy-input fallback.

On 1,000 public training tasks, the frozen predictions matched 49/1,076 test
outputs (4.55%) in 15.67 seconds. This is a training-data development measurement,
not unseen generalization. Hosted notebook
`kunalsinghh25/arc-hydra-arc2-symbolic-baseline/1` completed and generated valid
outputs for all 240 supplied tasks / 259 test outputs. IDs and output counts
matched the sample submission. Official submission **57747726 completed at
0.00**, with no reported error. No per-task official diagnostics are available.
This solver remains a reproducible floor and fallback, not a competitive choice.

## Neural path

The public Apache-2.0 checkpoint is
`sorokin/qwen3_4b_grids15_sft139/Transformers/bfloat16/1`, about 7.27 GB on disk.
Its 16-token grid vocabulary is different from the general-language ARC-AGI-3
model; it is not a drop-in replacement for the game-playing Python agent.

`arc2/neural.py` uses standard Transformers FP16 inference, exact grid/chat
serialization, identity/transpose views and a generation grammar for rectangular
digit grids. It rejects unfinished/invalid output and records omissions, timeouts
and memory errors. This is a new inference-only baseline, not reproduction of
the full published NVARC method or its reported scores. Public notebook
`jingshuifu/arc-agi-2-solution-v2` was inspected as a reference; its latest code
contains additional induction changes, so its earlier reported 28.89 must not
be attributed to our implementation.

`kunalsinghh03/arc-hydra-arc2-neural-development/1` is RUNNING on verified real
T4 hardware. It loaded the checkpoint and emitted actual generation tokens.
It benchmarks all 1,000 public training tasks with a 12-hour maximum including
startup and a ten-minute finalization reserve. Predictions are frozen before
training solution labels are read. The pretrained checkpoint may have seen
these public tasks; any eventual score is not a held-out result.

## Task-local learning and matched comparison

`arc2/adaptation.py` adds rank-16 LoRA updates to 33,030,144 parameters; base
weights stay frozen. Training uses only supplied demonstration pairs, masking
input/header tokens from the loss. Geometry and color augmentations preserve
input/output correspondence. Adapters reset between puzzles.

Actual GPU probe version 1 failed before training because stock TorchAO 0.10.0
was incompatible with PEFT's minimum 0.16.0. Version 2 removed that unused
optional quantization backend; this path uses plain FP16 LoRA. Both tasks then
completed all eight requested steps, changed adapter weights, reset exactly and
produced valid grids. Peak allocated GPU memory was 7,845,596,160 bytes (7.31
GiB). Lower training losses and passing these checks do not establish improved
prediction accuracy.

`kunalsinghh03/arc-hydra-arc2-adaptation-comparison/1` is RUNNING: same model/GPU,
grammar and prediction views before and after adaptation on 50 fixed public
training tasks. It will report paired improvements and regressions after both
prediction files are frozen. This determines whether the small adaptation
should proceed to a competition candidate. It does not certify hidden transfer.

## Boundaries and resources

Automatic approval review rejected downloading `arc-agi_evaluation_solutions.json`
as potentially sensitive hidden-answer data that was not specifically authorized.
That download remains blocked. It was not retried through another endpoint.
Only explicitly permitted public training challenges/solutions and the sample
submission were downloaded. Official evaluations provide separate score evidence.

The user-designated compute account hosts private development notebooks using
public training inputs and publicly licensed weights. It makes no competition
entries or submissions. Account-rule compliance is not certified by technical
access. Each of the two active neural runs is capped at 12 hours, for at most
24 hours plus short probes within the observed 30-hour free allowance; paid
scaling is disabled. Original-account submissions remain separate.

The separate ARC-AGI-3 control/inspection versions both terminated before
inference: the requested RTX configuration had no NVIDIA driver. A standard
T4 probe successfully returned two real T4s. This diagnoses available hardware
but does not explain the exact backend mapping issue or make the large ARC-3
configuration compatible with T4 unchanged. No gameplay score is assigned to
those failed runs. ARC-3's best official score remains 28.45.
