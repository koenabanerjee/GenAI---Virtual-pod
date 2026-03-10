# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260310_145207_diabetesai\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260310_145207_diabetesai\testing\tests\test_integration_generated_app.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_integration_generated_app.py:5: in <module>
    from generated_app.diabetes_prediction_system_integration_with_ehr import build_diabetes_prediction_system_integration_with_ehr
development\generated_app\diabetes_prediction_system_integration_with_ehr.py:5: in <module>
    import hl7.fhir as fhir
E   ModuleNotFoundError: No module named 'hl7'
=========================== short test summary info ===========================
ERROR testing/tests/test_integration_generated_app.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 1.18s
```

## Stderr
```text

```
