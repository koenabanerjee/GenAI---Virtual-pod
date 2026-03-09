# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
_ ERROR collecting testing/tests/test_ai_virtual_development_team_auto_create_tests.py _
C:\Users\Koena\AppData\Roaming\Python\Python313\site-packages\_pytest\python.py:507: in importtestmodule
    mod = import_path(
C:\Users\Koena\AppData\Roaming\Python\Python313\site-packages\_pytest\pathlib.py:587: in import_path
    importlib.import_module(module_name)
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
<frozen importlib._bootstrap>:1387: in _gcd_import
    ???
<frozen importlib._bootstrap>:1360: in _find_and_load
    ???
<frozen importlib._bootstrap>:1331: in _find_and_load_unlocked
    ???
<frozen importlib._bootstrap>:935: in _load_unlocked
    ???
C:\Users\Koena\AppData\Roaming\Python\Python313\site-packages\_pytest\assertion\rewrite.py:188: in exec_module
    source_stat, co = _rewrite_test(fn, self.config)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Users\Koena\AppData\Roaming\Python\Python313\site-packages\_pytest\assertion\rewrite.py:357: in _rewrite_test
    tree = ast.parse(source, filename=strfn)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Python313\Lib\ast.py:54: in parse
    return compile(source, filename, mode, flags,
E     File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests\test_ai_virtual_development_team_auto_create_tests.py", line 41
E       assert test["test_name"] == f"test_{test_data['user_story']}_acceptance_criteria_{''.join(map(str, [i for i in range(len(test_data['acceptance_criteria'])]))}"
E                                                                                                                                                                 ^
E   SyntaxError: closing parenthesis ']' does not match opening parenthesis '('
_ ERROR collecting testing/tests/test_ai_virtual_development_team_receive_business_requirements.py _
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests\test_ai_virtual_development_team_receive_business_requirements.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_ai_virtual_development_team_receive_business_requirements.py:26: in <module>
    from generated_app import ai_virtual_development_team
E   ImportError: cannot import name 'ai_virtual_development_team' from 'generated_app' (C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\development\generated_app\__init__.py)
_ ERROR collecting testing/tests/test_ai_virtual_development_team_report_progress_to_pm.py _
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests\test_ai_virtual_development_team_report_progress_to_pm.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_ai_virtual_development_team_report_progress_to_pm.py:2: in <module>
    from generated_app.ai_virtual_development_team import AIVirtualDevelopmentTeam
E   ModuleNotFoundError: No module named 'generated_app.ai_virtual_development_team'
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests\test_integration_generated_app.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_integration_generated_app.py:2: in <module>
    from ai_virtual_development_team.generated_app import build_receive_business_requirements, build_generate_user_stories, \
E   ModuleNotFoundError: No module named 'ai_virtual_development_team'
=========================== short test summary info ===========================
ERROR testing/tests/test_ai_virtual_development_team_auto_create_tests.py
ERROR testing/tests/test_ai_virtual_development_team_receive_business_requirements.py
ERROR testing/tests/test_ai_virtual_development_team_report_progress_to_pm.py
ERROR testing/tests/test_integration_generated_app.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!
4 errors in 0.35s
```

## Stderr
```text

```
