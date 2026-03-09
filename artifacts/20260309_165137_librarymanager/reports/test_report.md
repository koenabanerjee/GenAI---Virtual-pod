# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_165137_librarymanager\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_165137_librarymanager\testing\tests\test_integration_generated_app.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_integration_generated_app.py:4: in <module>
    from generated_app.issue_and_return_books import build_issue_and_return_books
development\generated_app\issue_and_return_books.py:9: in <module>
    from library_management_system import Book, LibraryManagementSystem
E   ModuleNotFoundError: No module named 'library_management_system'
=========================== short test summary info ===========================
ERROR testing/tests/test_integration_generated_app.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.30s
```

## Stderr
```text

```
