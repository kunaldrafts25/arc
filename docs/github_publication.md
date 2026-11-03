# GitHub publication and original commit history

The complete workspace is published at https://github.com/kunaldrafts25/arc.
The separate scoped repositories are https://github.com/kunaldrafts25/arc3
and https://github.com/kunaldrafts25/arc2.

The original development branch is `feature/arc-hydra-v03-model`. It preserves
commit `f561c06e469758d7011ceff58f5513b9051b6a53`, all55 subsequent existing
commits through `53f8626`, and a new checkpoint of the current working files.
It is pushed as a directly browsable branch in the combined repository.
`main` retains the combined workspace layout and the separately published data.

The original starter remote is retained as `upstream`; `origin` now points to
`https://github.com/kunaldrafts25/arc.git`. Future updates on this development
branch can use ordinary `git add`, `git commit`, and `git push`.

The319 adapter/raw-data artifacts remain in the free GitHub Releases and are
mapped by `ARTIFACTS.json`; the large payloads are intentionally kept out of
normal Git. `python scripts/restore_artifacts.py --verify-only` checks the
local artifact copies. Credentials, environments and disposable caches remain
ignored. The live Kaggle observer state changes each minute and is ignored;
its initial publication snapshot remains available in the published repositories.

No fork is required: the three destinations are owned by kunaldrafts25.
