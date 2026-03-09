# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_171313_demo\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_171313_demo\testing\tests\test_integration_generated_app.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_integration_generated_app.py:3: in <module>
    from generated_app.develop_a_feature_to_analyze_student_data_for_performance_predic import build_develop_a_feature_to_analyze_student_data_for_performance_predic
E   ImportError: cannot import name 'build_develop_a_feature_to_analyze_student_data_for_performance_predic' from 'generated_app.develop_a_feature_to_analyze_student_data_for_performance_predic' (C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_171313_demo\development\generated_app\develop_a_feature_to_analyze_student_data_for_performance_predic.py)
=========================== short test summary info ===========================
ERROR testing/tests/test_integration_generated_app.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 5.36s
```

## Stderr
```text

```
