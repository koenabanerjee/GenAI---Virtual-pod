# Test Execution Report

## Command
`C:\Python313\python.exe <builtin-test-runner> C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests`

## Return Code
1

## Stdout
```text
summary: 0 passed, 11 failed (builtin-test-runner)
```

## Stderr
```text
FAIL test_business_requirements.py::test_module_imports
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_business_requirements.py", line 7, in test_module_imports
    module = importlib.import_module("generated_app.business_requirements")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_business_requirements.py::test_module_wrapper_returns_dict
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_business_requirements.py", line 12, in test_module_wrapper_returns_dict
    module = importlib.import_module("generated_app.business_requirements")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

Failed importing test_integration_generated_app.py
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 211, in _run_builtin_tests
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_integration_generated_app.py", line 3, in <module>
    from generated_app.business_requirements import build_business_requirements
ModuleNotFoundError: No module named 'generated_app'

FAIL test_it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed.py::test_module_imports
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed.py", line 7, in test_module_imports
    module = importlib.import_module("generated_app.it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed.py::test_module_wrapper_returns_dict
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed.py", line 12, in test_module_wrapper_returns_dict
    module = importlib.import_module("generated_app.it_should_auto_create_unit_and_integration_tests_execute_them_and_produce_detailed")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_it_should_generate_python_implementation_modules_using_enterprise_coding_templates.py::test_module_imports
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_it_should_generate_python_implementation_modules_using_enterprise_coding_templates.py", line 7, in test_module_imports
    module = importlib.import_module("generated_app.it_should_generate_python_implementation_modules_using_enterprise_coding_templates")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_it_should_generate_python_implementation_modules_using_enterprise_coding_templates.py::test_module_wrapper_returns_dict
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_it_should_generate_python_implementation_modules_using_enterprise_coding_templates.py", line 12, in test_module_wrapper_returns_dict
    module = importlib.import_module("generated_app.it_should_generate_python_implementation_modules_using_enterprise_coding_templates")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full.py::test_module_imports
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full.py", line 7, in test_module_imports
    module = importlib.import_module("generated_app.the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full.py::test_module_wrapper_returns_dict
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full.py", line 12, in test_module_wrapper_returns_dict
    module = importlib.import_module("generated_app.the_organization_needs_an_ai_powered_virtual_development_pod_that_automates_the_full")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance.py::test_module_imports
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance.py", line 7, in test_module_imports
    module = importlib.import_module("generated_app.the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'

FAIL test_the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance.py::test_module_wrapper_returns_dict
Traceback (most recent call last):
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\src\virtual_dev_pod\agents\tester.py", line 225, in _run_builtin_tests
    fn()
    ~~^^
  File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_140805_demo\testing\tests\test_the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance.py", line 12, in test_module_wrapper_returns_dict
    module = importlib.import_module("generated_app.the_system_should_convert_high_level_requirements_into_structured_user_stories_and_acceptance")
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'generated_app'
```
