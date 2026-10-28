import json
from pathlib import Path
from uuid import uuid4

import pytest

from scripts.build_compute_control import package,resolver_source


@pytest.mark.parametrize('legacy',[False,True])
def test_nested_public_wheelhouse_resolves_with_canonical_and_short_mounts(legacy):
    root=Path(__file__).resolve().parents[1]/'test-artifacts'/('compute-input-'+uuid4().hex)
    root.mkdir(parents=True)
    values={};definitions=[('WHEELHOUSE_DIR','runtime','requirements.lock',''),
        ('ORIG_BUNDLE_DIR','source','src/ARC3-Inference/inference/agent/tool_agent.py',''),
        ('COMPETITION_WHEELHOUSE','public','arc_agi-0.9.8.whl','arc_agi_3_wheels')]
    for key,name,marker,suffix in definitions:
        canonical=root/'datasets/owner'/name/suffix
        actual=(root/name/suffix) if legacy else canonical
        file=actual/marker;file.parent.mkdir(parents=True,exist_ok=True);file.write_text('synthetic marker')
        values[key]=str(canonical)
    for key,name in [('MODEL_DIR','target'),('DRAFT_MODEL_DIR','draft')]:
        canonical=root/'models/owner'/name/'transformers/default/1'
        actual=(root/name/'transformers/default/1') if legacy else canonical
        actual.mkdir(parents=True,exist_ok=True);(actual/'config.json').write_text('{}');values[key]=str(canonical)
    ns={};exec(resolver_source(),ns)
    resolved=ns['resolve_inputs'](values,root)
    assert Path(resolved['COMPETITION_WHEELHOUSE']).name=='arc_agi_3_wheels'
    assert all(Path(path).is_dir() for path in resolved.values())


@pytest.mark.parametrize('kind',['control','inspection'])
def test_compute_package_has_no_competition_attachment_and_validates_public_inputs(kind):
    notebook,metadata,provenance=package(kind)
    assert metadata['competition_sources']==[] and metadata['id'].startswith('kunalsinghh03/')
    assert provenance['notebook_wall_budget_seconds']==32400
    config=next(c['source'] for c in notebook['cells'] if c['source'].startswith('import json\nimport os'))
    assert 'This notebook is public development only' in config
    checks=config.split('from hashlib import sha256 as _hydra_public_sha',1)[1].split('# Apply harness patch',1)[0]
    checks='from hashlib import sha256 as _hydra_public_sha'+checks
    root=Path(__file__).resolve().parents[1]
    exec(compile(checks,'public-compute-input-checks','exec'),dict(Path=Path,json=json,
        COMPETITION_WHEELHOUSE=str(root/'reference/public-development-inputs/arc_agi_3_wheels')))
    assert 'KGAT_' not in json.dumps(notebook)
