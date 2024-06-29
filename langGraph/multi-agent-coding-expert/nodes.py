
from app import coder, refine_code, executer, tester_agent

def programmer(state):
    print(f'Entering in Programmer')
    requirement = state['requirement']
    code_ = coder.invoke({'requirement':requirement})
    return {'code':code_.code}

def debugger(state):
    print(f'Entering in Debugger')
    errors = state['errors']
    code = state['code']
    refine_code_ = refine_code.invoke({'code':code,'error':errors})
    return {'code':refine_code_.code,'errors':None}

def executer(state):
    print(f'Entering in Executer')
    tests = state['tests']
    input_ = tests['input']
    output_ = tests['output']
    code = state['code']
    executable_code = executer.invoke({"code":code,"input":input_,'output':output_})
    #print(f"Executable Code - {executable_code.code}")
    error = None
    try:
        exec(executable_code.code)
        print("Code Execution Successful")
    except Exception as e:
        print('Found Error While Running')
        error = f"Execution Error : {e}"
    return {'code':executable_code.code,'errors':error}

def tester(state):
    print(f'Entering in Tester')
    requirement = state['requirement']
    code = state['code']
    tests = tester_agent.invoke({'requirement':requirement,'code':code})
    #tester.invoke({'requirement':'Generate fibbinaco series','code':code_.code})
    return {'tests':{'input':tests.Input,'output':tests.Output}}

def decide_to_end(state):
    print(f'Entering in Decide to End')
    if state['errors']:
        return 'debugger'
    else:
        return 'end'