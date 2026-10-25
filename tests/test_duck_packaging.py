import json
from datetime import datetime
from types import SimpleNamespace
from scripts.build_duck_notebook import build, SOURCE
from scripts.analyze_duck_run import summarize, reconcile_tokens


def controls(notebook):
    return next(c['source'] for c in notebook['cells']
                if c['source'].startswith('# Make one-off changes'))


def config(source, submission):
    bm = SimpleNamespace(solver=SimpleNamespace())
    namespace = dict(bm=bm, TRUE_SUBMISSION=submission, USE_PRIORITY_SCHEDULING=True,
                     target=SimpleNamespace(max_runtime_s=32400.0))
    exec(compile(source,'duck-controls','exec'),namespace)
    return bm


def test_preflight_limits_never_replace_contest_controls():
    notebook, metadata, provenance = build()
    original = json.loads(SOURCE.read_text(encoding='utf-8'))
    for cell in original['cells']:
        cell['source'] = ''.join(cell['source'])
    prior = config(controls(original), True)
    contest = config(controls(notebook), True)
    assert vars(contest.solver) == vars(prior.solver)
    assert contest.n_passes == prior.n_passes == 1
    assert contest.solver.concurrency == 120
    assert contest.solver.max_runtime_s_per_game == 31920
    public = config(controls(notebook), False)
    assert public.n_passes == 1
    assert public.solver.max_runtime_s_per_game == 900
    assert metadata['is_private'] and not metadata['enable_internet']
    assert len(metadata['model_sources']) == 2
    assert metadata['machine_shape'] == 'NvidiaRtxPro6000'
    assert provenance['source_sha256'] == '88a379f17c3a4ba8c98715fc23155346ccd6eb289bdafebadfc61a3178f9d9bd'


def test_agent_serving_and_prompts_are_unchanged_in_reproduction():
    notebook, _, _ = build()
    original = json.loads(SOURCE.read_text(encoding='utf-8'))
    original_code = [''.join(c['source']) for c in original['cells'] if c['cell_type']=='code']
    derived_code = [c['source'] for c in notebook['cells'] if c['cell_type']=='code']
    assert len(original_code) == len(derived_code)
    changed = [(a,b) for a,b in zip(original_code,derived_code) if a!=b]
    assert len(changed)==2
    assert changed[0][1].startswith(changed[0][0])
    assert changed[1][0].startswith("print('Starting benchmark...')")
    assert all(not c.get('outputs') for c in notebook['cells'])


def test_warmup_reset_cannot_be_misreported_as_model_gameplay():
    row = dict(game_id='unseen',state='cancelled',actions=1,generated_tokens=0,
               levels_completed=0,total_levels=6,score=0,note='deadline')
    assert not summarize([row])['model_gameplay_verified']
    row.update(actions=15,generated_tokens=4000,levels_completed=1,score=1.2)
    result=summarize([row])
    assert result['model_gameplay_verified']
    assert result['mean_public_score']==1.2
    assert result['full_wins']==0


def test_public_model_wait_never_runs_in_a_competition_rerun():
    notebook, _, _ = build()
    source=next(c['source'] for c in notebook['cells'] if c['source'].startswith("print('Starting benchmark...')"))
    evaluation=source.split('# ARC-Hydra public reproduction; no hidden game selection.\n',1)[1]
    evaluation=evaluation.split('await bm.run(',1)[0]
    # No public model-health call, game filter or deadline replacement is
    # allowed on the competition path. Missing variables deliberately catch it.
    exec(compile(evaluation,'public-readiness-gate','exec'),dict(TRUE_SUBMISSION=True))


def test_final_turn_tokens_are_not_mistaken_for_total_generation():
    rows=[dict(game_id='game',generated_tokens=0)]
    runs=[dict(game_id='game',history=[dict(generated_tokens=120),dict(generated_tokens=80)],
               final_generated_tokens=20)]
    corrected, changes=reconcile_tokens(rows,runs)
    assert rows[0]['generated_tokens']==0  # preserve raw downloaded evidence
    assert corrected[0]['generated_tokens']==220
    assert changes==[dict(game_id='game',reported_tokens=0,reconstructed_tokens=220)]


def test_competition_finalization_budget_includes_model_startup():
    notebook, _, provenance=build('benchmark',contest_reserve_seconds=600)
    source=next(c['source'] for c in notebook['cells'] if c['source'].startswith("print('Starting benchmark...')"))
    gate=source.split('# ARC-Hydra bounded competition finalization.\n',1)[1].split('await bm.run(',1)[0]
    start_epoch=1700000000
    namespace=dict(TRUE_SUBMISSION=True,NOTEBOOK_START_TIME=start_epoch,
                   target=SimpleNamespace(max_runtime_s=32400),datetime=datetime)
    exec(compile(gate,'contest-deadline','exec'),namespace)
    assert namespace['soft_end'].timestamp()==start_epoch+32400-600
    # Even after 33 minutes of setup, ten minutes remain for cancellation and
    # output writing; a fresh per-game nine-hour timer cannot extend this cap.
    assert namespace['soft_end'].timestamp()-(start_epoch+33*60)==32400-600-33*60
    assert provenance['competition_finalization_reserve_seconds']==600
