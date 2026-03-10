# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260310_150503_attendancetracker\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
testing\tests\test_integration_generated_app.py:3: in <module>
    from generated_app.student_attendance_marking import build_student_attendance_marking
development\generated_app\student_attendance_marking.py:6: in <module>
    @dataclass
     ^^^^^^^^^
E   NameError: name 'dataclass' is not defined
=========================== short test summary info ===========================
ERROR testing/tests/test_integration_generated_app.py - NameError: name 'data...
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.18s
```

## Stderr
```text

```
