# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_162731_bakeryai\testing\tests`

## Return Code
2

## Stdout
```text
=================================== ERRORS ====================================
______ ERROR collecting testing/tests/test_integration_generated_app.py _______
testing\tests\test_integration_generated_app.py:2: in <module>
    from generated_app import manage_product_catalog as mpc, process_customer_orders as pco, \
development\generated_app\manage_product_catalog.py:8: in <module>
    @dataclass
     ^^^^^^^^^
E   NameError: name 'dataclass' is not defined
________ ERROR collecting testing/tests/test_manage_product_catalog.py ________
testing\tests\test_manage_product_catalog.py:2: in <module>
    from generated_app.manage_product_catalog import build_manage_product_catalog
development\generated_app\manage_product_catalog.py:8: in <module>
    @dataclass
     ^^^^^^^^^
E   NameError: name 'dataclass' is not defined
____ ERROR collecting testing/tests/test_manage_suppliers_and_employees.py ____
ImportError while importing test module 'C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_162731_bakeryai\testing\tests\test_manage_suppliers_and_employees.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python313\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
testing\tests\test_manage_suppliers_and_employees.py:3: in <module>
    from generated_app.manage_suppliers_and_employees.models import Supplier, Employee
E   ModuleNotFoundError: No module named 'generated_app.manage_suppliers_and_employees.models'; 'generated_app.manage_suppliers_and_employees' is not a package
___ ERROR collecting testing/tests/test_track_inventory_of_raw_materials.py ___
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
C:\Users\Koena\AppData\Roaming\Python\Python313\site-packages\_pytest\assertion\rewrite.py:197: in exec_module
    exec(co, module.__dict__)
testing\tests\test_track_inventory_of_raw_materials.py:2: in <module>
    from generated_app.track_inventory_of_raw_materials import build_track_inventory_of_raw_materials
E     File "C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260309_162731_bakeryai\development\generated_app\track_inventory_of_raw_materials.py", line 22
E       """Initialize InventoryService with an optional list of inventory records."""
E       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   IndentationError: expected an indented block after function definition on line 21
=========================== short test summary info ===========================
ERROR testing/tests/test_integration_generated_app.py - NameError: name 'data...
ERROR testing/tests/test_manage_product_catalog.py - NameError: name 'datacla...
ERROR testing/tests/test_manage_suppliers_and_employees.py
ERROR testing/tests/test_track_inventory_of_raw_materials.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!
4 errors in 0.55s
```

## Stderr
```text

```
