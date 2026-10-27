"""CPU/Linux smoke tests against the actual installed sandbox RPC runner."""
import json
import ast
import os
from pathlib import Path


def check_prompt(agent_source):
    from inference.agent import prompts
    function=next(n for n in ast.parse(agent_source).body if isinstance(n,ast.FunctionDef) and n.name=='_build_system_prompt')
    namespace=dict(vars(prompts))
    false=lambda *args,**kwargs:False
    namespace.update(os=os,_AUTO_FRAME_DIFF=False,_DIFF_IMAGE=False,
        _explain_gameplay_changed=false,_animation_enabled=false,current_grid_image_enabled=false,
        _get_env_bool=false,_persistent_functions=false,_memory_sections_disabled=lambda:True,
        _prefer_tool_calls=false,_level_transfer_guidance_enabled=false)
    exec(compile(ast.Module(body=[function],type_ignores=[]),'installed-prompt','exec'),namespace)
    prompt=namespace['_build_system_prompt'](tool_output_tokens=3072)
    assert 'You can also call `action(...)` multiple times' not in prompt
    assert 'Call `action(actions)` to execute one or more' not in prompt
    assert 'execute_plan(actions, predict' in prompt
    assert 'One exploratory `action(...)` call' in prompt
    return prompt


def run_probe():
    from inference.agent.python_tool_sandbox import run_sandboxed_python

    increment="def predict(state, action):\n    return [[state[0][0]+1]]\n"
    cases=[
        dict(name='consistent_plan',code=increment+"result=execute_plan(['RIGHT','RIGHT'],predict)",spent=2,reason='complete'),
        dict(name='retrospective_counterexample',code="def predict(state,action):\n    return [[99]]\nresult=execute_plan(['RIGHT','RIGHT'],predict)",spent=0,reason='unverified_model'),
        dict(name='prospective_counterexample',code=increment+"result=execute_plan(['RIGHT','RIGHT'],predict)",surprise=True,spent=1,reason='prediction_mismatch'),
        dict(name='zero_coverage',code=increment+"result=execute_plan(['RIGHT'],predict)",empty=True,spent=0,reason='unverified_model'),
        dict(name='constant_abstraction',code="def predict(state,action):\n    return 0\ndef encode(grid):\n    return 0\nresult=execute_plan(['RIGHT'],predict,encode)",spent=0,reason='unverified_model'),
        dict(name='impure_prediction',code="def predict(state,action_dict):\n    action('RIGHT')\n    return [[1]]\nresult=execute_plan(['RIGHT'],predict)",spent=0,reason='unverified_model'),
        dict(name='one_exploratory_action',code="action('RIGHT')\naction('RIGHT')",spent=1,error=True),
    ]
    reports=[]
    for case in cases:
        value=1
        calls=[]
        def view(number):
            return dict(grid=[[number]],ascii=str(number),shape=[1,1],step=number,level=1)
        history=[dict(action='',frame=view(0)),dict(action='RIGHT',frame=view(1))]
        def state():
            return dict(current_frame=view(value),history=list(history) if not case.get('empty') else [],valid_actions=['RIGHT'])
        def handler(actions,**kwargs):
            nonlocal value
            assert len(actions)==1
            calls.extend(actions)
            value=7 if case.get('surprise') else value+1
            history.append(dict(action='RIGHT',frame=view(value)))
            return dict(action_result=dict(executed=True,gameplay_changed=True),state=state())
        result=run_sandboxed_python(code=case['code'],timeout_seconds=5,
            initial_state=state(),action_handler=handler)
        assert len(calls)==case['spent'],(case['name'],result,calls)
        if case.get('error'):
            assert 'One exploratory' in result['error'],result
        else:
            assert not result['error'],result
            assert result['result']['stop_reason']==case['reason'],result
        events=result.get('hydra_verified_events')
        assert events,(case['name'],'missing mechanical event propagation')
        reports.append(dict(name=case['name'],passed=True,actual_actions=len(calls),events=events))
    from inference.agent import python_tool_sandbox
    agent_file=Path(python_tool_sandbox.__file__).with_name('tool_agent.py')
    check_prompt(agent_file.read_text(encoding='utf-8'))
    output=dict(passed=True,cases=reports,prompt_contract_consistent=True,boundary='Synthetic CPU integration checks of installed sandbox and prompt contract; no model inference, gateway or ARC gameplay tested')
    Path('/kaggle/working/verified-probe.json').write_text(json.dumps(output,indent=2)+'\n')
    print('VERIFIED_AGENT_CPU_PROBE_PASSED',json.dumps(dict(cases=len(reports))),flush=True)
    return output
