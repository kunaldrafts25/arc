"""Assemble compiler wheels into a CUDA toolkit prefix.

Adapted from Daniel Franzen's Apache-2.0 make_cuda_overlay.py, distributed
with arc-agi-3-solution. License: baselines/duck_m2/LICENSE.
"""
import importlib.metadata as md
from pathlib import Path
import subprocess
import sys

root=Path(sys.argv[1]).absolute()
root.mkdir()
for dist in sorted(md.distributions(),key=lambda d:d.metadata['Name']):
    if not dist.metadata['Name'].lower().replace('_','-').startswith('nvidia-'):
        continue
    for entry in dist.files or ():
        parts=entry.parts
        if len(parts)<4 or parts[0]!='nvidia' or parts[2] not in ('bin','include','lib','lib64','nvvm'):
            continue
        source=Path(dist.locate_file(entry)).absolute()
        if not source.is_file():
            continue
        dest=root/('lib64' if parts[2]=='lib' else parts[2])/Path(*parts[3:])
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists() or dest.is_symlink():
            if dest.read_bytes()!=source.read_bytes():
                raise RuntimeError(f'Conflicting CUDA files: {dest}')
        else:
            dest.symlink_to(source)
(root/'lib').symlink_to('lib64')
for name in ('bin/nvcc','bin/ptxas','include/cuda.h','include/cuda_runtime.h',
             'include/crt/host_config.h','nvvm/libdevice/libdevice.10.bc'):
    assert (root/name).is_file(),name
assert (root/'include/cccl/cuda/std').is_dir()
version=subprocess.check_output([str(root/'bin/nvcc'),'--version'],text=True)
assert 'release 13.3,' in version,version
print(version)
