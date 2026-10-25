"""Package the attributed public Franzen M2 baseline for offline Kaggle runs.

Defaults reproduce the agent. Optional runtime, deadline and memory experiments
are declared separately in provenance and use distinct notebook IDs.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'baselines/duck_m2/upstream.ipynb'
SOURCE_META = SOURCE.with_name('upstream-metadata.json')
PREFIXES = ('ft09', 'ls20', 'r11l', 'vc33', 'bp35')


def build(mode='preflight', contest_reserve_seconds=None, runtime_overlay_dataset=None, runtime_overlay_sha256=None, agent_variant='baseline'):
    if mode not in ('preflight', 'benchmark'):
        raise ValueError(mode)
    if agent_variant not in ('baseline','rolling-summary'):
        raise ValueError(agent_variant)
    if agent_variant!='baseline' and runtime_overlay_dataset is not None:
        raise ValueError('Evaluate memory and runtime changes separately first')
    if contest_reserve_seconds is not None and not 120 <= contest_reserve_seconds < 32400:
        raise ValueError('Contest finalization reserve must be between 120 and 32399 seconds')
    if runtime_overlay_dataset is not None:
        if not re.fullmatch(r'[A-Za-z0-9_-]+/[A-Za-z0-9_-]+',runtime_overlay_dataset):
            raise ValueError('Runtime overlay needs an owner/dataset reference')
        if runtime_overlay_sha256 is None or not re.fullmatch(r'[a-f0-9]{64}',runtime_overlay_sha256):
            raise ValueError('Runtime overlay requires the actual manifest SHA-256')
    elif runtime_overlay_sha256 is not None:
        raise ValueError('Manifest SHA requires a runtime overlay dataset')
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
    if agent_variant=='rolling-summary':
        overrides=dict(ARC3_SUMMARY_INTERVAL_TOKENS=48*1024,ARC3_SUMMARY_MAX_GEN=4096,
                       ARC3_SUMMARY_TURN_CONTEXT='1',ARC3_DRAIN_STOP_AT_SUMMARIES='1')
        configuration=next(c for c in notebook['cells'] if '\nos.environ.update({k: str(v) for k,v in setup_env.items()})' in c['source'])
        anchor='os.environ.update({k: str(v) for k,v in setup_env.items()})'
        assert configuration['source'].count(anchor)==1
        configuration['source']=configuration['source'].replace(anchor,
            '# ARC-Hydra rolling-summary experiment.\nsetup_env.update('+repr(overrides)+')\n'+anchor)
        provenance.update(agent_variant=agent_variant,agent_environment_overrides=overrides)
        provenance['competition_changes']='Periodic summaries and summary-aware context draining; original model, serving, tools and scheduler retained'
        if contest_reserve_seconds is not None:
            provenance['competition_changes']+=f'; {contest_reserve_seconds}-second finalization reserve'
    if runtime_overlay_dataset is not None:
        provenance.update(runtime_overlay_dataset=runtime_overlay_dataset,
                          runtime_overlay_manifest_sha256=runtime_overlay_sha256,
                          runtime_source_commit='560edbdca18aedae13f71ae20b3984efa4d22633')
        provenance['competition_changes'] = 'v3 serving overlay; original checkpoints, prompts, tools and agent settings retained'
        if contest_reserve_seconds is not None:
            provenance['competition_changes'] += f'; {contest_reserve_seconds}-second notebook finalization reserve'
        serving=next(c for c in notebook['cells'] if c['source'].startswith('# Paste this entire file into the launcher cell.'))
        anchor='# Report the optional later caching patch. This cell does not modify wheel code.'
        assert serving['source'].count(anchor)==1
        installer=(ROOT/'scripts/serving_v3/install_overlay.py').read_text(encoding='utf-8')
        hook='\n# ARC-Hydra: verified, offline serving overlay in a separate candidate.\n'
        hook+=f'HYDRA_OVERLAY_DATASET = {runtime_overlay_dataset!r}\n'
        hook+='hydra_overlay_options = [Path("/kaggle/input/datasets") / HYDRA_OVERLAY_DATASET, Path("/kaggle/input") / HYDRA_OVERLAY_DATASET.split("/")[1]]\n'
        hook+='hydra_overlay = next((p for p in hydra_overlay_options if (p / "manifest.json").is_file()), None)\n'
        hook+='if hydra_overlay is None:\n    raise RuntimeError("Runtime overlay dataset not mounted")\n'
        hook+=f'if sha256(hydra_overlay / "manifest.json") != {runtime_overlay_sha256!r}:\n    raise RuntimeError("Runtime overlay manifest differs from tested build")\n'
        hook+='hydra_installer = Path(PREFIX) / "install_v3_overlay.py"\n'
        hook+=f'hydra_installer.write_text({installer!r})\n'
        hook+='hydra_runtime_env = Path(PREFIX) / "v3_environment.json"\n'
        hook+='run([sys.executable, hydra_installer, "--overlay", hydra_overlay, "--base", WHEELHOUSE_DIR, "--venv", VENV, "--uv", Path(PREFIX) / "bin/uv", "--environment-output", hydra_runtime_env, "--port", SERVED_MODEL_PORT], env=env)\n'
        hook+='env.update(json.loads(hydra_runtime_env.read_text()))\n'
        hook+='CUDA_HOME, CC, CXX = env["CUDA_HOME"], env["CC"], env["CXX"]\n'
        hook+='run([env["CUDACXX"], "--version"], env=env)\n'
        hook+='print("Overlay host compiler:", env["CXX"])\n\n'
        serving['source']=serving['source'].replace(anchor,hook+anchor)
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
    configuration_note=('Published serving configuration retained. ' if runtime_overlay_dataset is None else
                        'Experimental v3 serving overlay; GPU correctness and performance unverified. ')
    configuration_note+=('Original competition time controls retained.' if contest_reserve_seconds is None else
                         f'Contest deadline includes startup and reserves {contest_reserve_seconds} seconds for finalization.')
    if agent_variant=='rolling-summary':
        configuration_note+=' Experimental periodic summaries with summary-aware history draining; benefit unproven.'
    notebook['cells'].insert(0, dict(cell_type='markdown', metadata={}, source=(
        '# ARC-Hydra: attributed Duck M2 reproduction\n\n'
        'Original agent and serving code: **Daniel Franzen**, building on '
        '**Jeroen Cottaar and Tufa Labs**. Apache-2.0; model/runtime terms apply.\n\n'
        'This private notebook measures the attributed agent or a declared runtime experiment. '
        f'Public mode: {mode}. {configuration_note} '
        'No score reproduction or score above 71 is claimed.\n\n'
        '[Original notebook](https://www.kaggle.com/code/dfranzen/arc-agi-3-milestone-2-solution) · '
        '[Author source](https://github.com/da-fr/arc-agi-3-solution)\n')))
    metadata = json.loads(SOURCE_META.read_text())
    for key in ('id_no', 'keywords'):
        metadata.pop(key, None)
    metadata.update(id='kunalsinghh25/arc-hydra-duck-m2-baseline',
                    title='ARC Hydra Duck M2 Baseline', code_file='submission.ipynb',
                    is_private=True, enable_internet=False, machine_shape='NvidiaRtxPro6000')
    if runtime_overlay_dataset is not None:
        metadata['dataset_sources'].append(runtime_overlay_dataset)
        metadata['id']='kunalsinghh25/arc-hydra-duck-v3-runtime'
        metadata['title']='ARC Hydra Duck V3 Runtime'
    if agent_variant=='rolling-summary':
        metadata.update(id='kunalsinghh25/arc-hydra-duck-summary',title='ARC Hydra Duck Summary')
    return notebook, metadata, provenance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('preflight','benchmark'), default='preflight')
    parser.add_argument('--output')
    parser.add_argument('--contest-reserve-seconds',type=int)
    parser.add_argument('--runtime-overlay-dataset')
    parser.add_argument('--runtime-overlay-sha256')
    parser.add_argument('--agent-variant',choices=('baseline','rolling-summary'),default='baseline')
    args = parser.parse_args()
    notebook, metadata, provenance = build(args.mode,args.contest_reserve_seconds,args.runtime_overlay_dataset,args.runtime_overlay_sha256,args.agent_variant)
    output=args.output or ('notebooks/duck_summary' if args.agent_variant=='rolling-summary' else
                          'notebooks/duck_v3_runtime' if args.runtime_overlay_dataset else 'notebooks/duck_m2')
    destination = (ROOT/output).resolve()
    if not destination.is_relative_to(ROOT):
        raise ValueError('Notebook output must stay inside the workspace')
    destination.mkdir(parents=True,exist_ok=True)
    for name, value in (('submission.ipynb',notebook),('kernel-metadata.json',metadata),('provenance.json',provenance)):
        (destination/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(provenance,indent=2))


if __name__ == '__main__':
    main()
