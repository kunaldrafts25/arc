"""Package the attributed public Franzen M2 baseline for offline Kaggle runs.

The model, serving stack, prompts and competition controls remain upstream.
Only non-competition evaluation scope and result validation are changed.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'baselines/duck_m2/upstream.ipynb'
SOURCE_META = SOURCE.with_name('upstream-metadata.json')
PREFIXES = ('ft09', 'ls20', 'r11l', 'vc33', 'bp35')


def build(mode='preflight', contest_reserve_seconds=None):
    if mode not in ('preflight', 'benchmark'):
        raise ValueError(mode)
    if contest_reserve_seconds is not None and not 120 <= contest_reserve_seconds < 32400:
        raise ValueError('Contest finalization reserve must be between 120 and 32399 seconds')
    upstream = json.loads(SOURCE.read_text(encoding='utf-8'))
    notebook = deepcopy(upstream)
    code_digests = []
    for cell in notebook['cells']:
        cell['source'] = ''.join(cell['source'])
        if cell['cell_type'] == 'code':
            code_digests.append(sha256(cell['source'].encode()).hexdigest())
            cell['outputs'] = []
            cell['execution_count'] = None
    provenance = dict(
        source='https://www.kaggle.com/code/dfranzen/arc-agi-3-milestone-2-solution',
        source_sha256=sha256(SOURCE.read_bytes()).hexdigest(),
        source_code_sha256=code_digests,
        author_repository='https://github.com/da-fr/arc-agi-3-solution',
        inspected_repository_commit='10882e332d883af3e61616df8c8a17d03a328a75',
        authors=['Daniel Franzen', 'Jeroen Cottaar', 'Tufa Labs'],
        license='Apache-2.0; third-party model/runtime licenses also apply',
        mode=mode, public_games=list(PREFIXES) if mode=='preflight' else 'all 25',
        public_runtime_seconds=900 if mode=='preflight' else 7200,
        public_startup_allowance_seconds=3600,
        competition_changes='None to model, prompts, tools, serving or scheduling',
    )
    if contest_reserve_seconds is not None:
        provenance['competition_finalization_reserve_seconds'] = contest_reserve_seconds
        provenance['competition_changes'] = 'Global notebook deadline with finalization reserve; agent/model/prompts/tools/serving/scheduling settings unchanged'
    controls = next(c for c in notebook['cells'] if c['source'].startswith('# Make one-off changes'))
    controls['source'] += '\n\n# ARC-Hydra: bound public evaluation only; retain contest settings.\n'
    controls['source'] += 'if not TRUE_SUBMISSION:\n    bm.n_passes = 1\n'
    controls['source'] += f'    bm.solver.max_runtime_s_per_game = {provenance["public_runtime_seconds"]}\n'
    controls['source'] += '    bm.solver.save_request_logs = True\n    bm.periodic_save_interval_s = 120\n'
    run = next(c for c in notebook['cells'] if c['source'].startswith("print('Starting benchmark...')"))
    needle = 'await bm.run(soft_end_time=soft_end, runtime_environment=target, minimal_diagnostics=TRUE_SUBMISSION)'
    assert run['source'].count(needle) == 1
    evaluation = '\n# ARC-Hydra public reproduction; no hidden game selection.\nif not TRUE_SUBMISSION:\n'
    wait_source = (ROOT/'scripts/wait_local_backend.py').read_text(encoding='utf-8')
    evaluation += f'    exec({wait_source!r})\n'
    evaluation += '    wait_local_backend(f"http://127.0.0.1:{SERVED_MODEL_PORT}/health", NOTEBOOK_START_TIME + 3600, proc)\n'
    if mode == 'preflight':
        evaluation += f'    hydra_prefixes = {PREFIXES!r}\n'
        evaluation += '    bm.games = [g for g in bm.games if g.env_name.split("-")[0] in hydra_prefixes]\n'
        evaluation += '    if len(bm.games) != len(hydra_prefixes):\n        raise RuntimeError("Public preflight games missing")\n'
    evaluation += '    bm.solver.concurrency = len(bm.games)\n'
    evaluation += f'    soft_end = datetime.now() + timedelta(seconds={provenance["public_runtime_seconds"]})\n'
    evaluation += '    print("Hydra effective public run:", dict(games=len(bm.games), passes=bm.n_passes, concurrency=bm.solver.concurrency, gameplay_seconds=bm.solver.max_runtime_s_per_game, deadline=soft_end.isoformat()))\n'
    evaluation += f'    Path(WORKING_DIR / "hydra_provenance.json").write_text(json.dumps({provenance!r}, indent=2))\n'
    if contest_reserve_seconds is not None:
        evaluation += '\n# ARC-Hydra bounded competition finalization.\nif TRUE_SUBMISSION:\n'
        evaluation += '    hydra_notebook_budget = float(target.max_runtime_s)\n'
        evaluation += f'    if not {contest_reserve_seconds} < hydra_notebook_budget:\n        raise RuntimeError("Notebook budget is smaller than finalization reserve")\n'
        evaluation += f'    soft_end = datetime.fromtimestamp(NOTEBOOK_START_TIME + hydra_notebook_budget - {contest_reserve_seconds})\n'
        evaluation += '    print("Competition soft deadline:", soft_end.isoformat(), "including notebook startup")\n'
    run['source'] = run['source'].replace(needle, evaluation+'\n'+needle)
    # Benchmark.run deliberately swallows some solver errors. A completed
    # notebook therefore needs an explicit gameplay/exception check.
    run['source'] += '''

if not TRUE_SUBMISSION:
    hydra_summary = [dict(game_id=r.game_id, state=r.state,
                          levels_completed=r.levels_completed,
                          total_levels=r.number_of_levels,
                          actions=sum(r.actions_per_level),
                          score=r.final_score,
                          generated_tokens=sum(a.generated_tokens for a in r.history)+r.final_generated_tokens,
                          note=r.solver_note) for r in bm.game_runs]
    (WORKING_DIR / 'hydra_model_summary.json').write_text(json.dumps(hydra_summary, indent=2))
    print(json.dumps(hydra_summary, indent=2))
    if not hydra_summary or any(r['state'] in ('crashed', 'not_started') or r['actions'] <= 0 for r in hydra_summary):
        raise RuntimeError('Model gameplay preflight failed; inspect benchmark.json and serve.log')
'''
    notebook['cells'].insert(0, dict(cell_type='markdown', metadata={}, source=(
        '# ARC-Hydra: attributed Duck M2 reproduction\n\n'
        'Original agent and serving code: **Daniel Franzen**, building on '
        '**Jeroen Cottaar and Tufa Labs**. Apache-2.0; model/runtime terms apply.\n\n'
        'This private notebook measures the published baseline before further changes. '
        f'Public mode: {mode}. Original competition settings are retained. '
        'No score reproduction or score above 71 is claimed.\n\n'
        '[Original notebook](https://www.kaggle.com/code/dfranzen/arc-agi-3-milestone-2-solution) · '
        '[Author source](https://github.com/da-fr/arc-agi-3-solution)\n')))
    metadata = json.loads(SOURCE_META.read_text())
    for key in ('id_no', 'keywords'):
        metadata.pop(key, None)
    metadata.update(id='kunalsinghh25/arc-hydra-duck-m2-baseline',
                    title='ARC Hydra Duck M2 Baseline', code_file='submission.ipynb',
                    is_private=True, enable_internet=False, machine_shape='NvidiaRtxPro6000')
    return notebook, metadata, provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('preflight','benchmark'), default='preflight')
    parser.add_argument('--output', default='notebooks/duck_m2')
    parser.add_argument('--contest-reserve-seconds',type=int)
    args = parser.parse_args()
    notebook, metadata, provenance = build(args.mode,args.contest_reserve_seconds)
    destination = (ROOT/args.output).resolve()
    if not destination.is_relative_to(ROOT):
        raise ValueError('Notebook output must stay inside the workspace')
    destination.mkdir(parents=True,exist_ok=True)
    for name, value in (('submission.ipynb',notebook),('kernel-metadata.json',metadata),('provenance.json',provenance)):
        (destination/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(provenance,indent=2))


if __name__ == '__main__':
    main()
