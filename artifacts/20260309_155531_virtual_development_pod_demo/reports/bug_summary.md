# Bug Summary Report

**Status:** FAIL

## Summary
Automated tests found defects.

## Details
- =================================== ERRORS ====================================
- _ ERROR collecting testing/tests/test_ai_virtual_development_team_auto_create_tests.py _
- E     File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\testing\tests\test_ai_virtual_development_team_auto_create_tests.py", line 41
- E       assert test["test_name"] == f"test_{test_data['user_story']}_acceptance_criteria_{''.join(map(str, [i for i in range(len(test_data['acceptance_criteria'])]))}"
- E                                                                                                                                                                 ^
- E   SyntaxError: closing parenthesis ']' does not match opening parenthesis '('
- _ ERROR collecting testing/tests/test_ai_virtual_development_team_receive_business_requirements.py _
- E   ImportError: cannot import name 'ai_virtual_development_team' from 'generated_app' (C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_155531_virtual_development_pod_demo\development\generated_app\__init__.py)
- _ ERROR collecting testing/tests/test_ai_virtual_development_team_report_progress_to_pm.py _
- E   ModuleNotFoundError: No module named 'generated_app.ai_virtual_development_team'
- ______ ERROR collecting testing/tests/test_integration_generated_app.py _______
- E   ModuleNotFoundError: No module named 'ai_virtual_development_team'
- ERROR testing/tests/test_ai_virtual_development_team_auto_create_tests.py
- ERROR testing/tests/test_ai_virtual_development_team_receive_business_requirements.py
- ERROR testing/tests/test_ai_virtual_development_team_report_progress_to_pm.py
- ERROR testing/tests/test_integration_generated_app.py
