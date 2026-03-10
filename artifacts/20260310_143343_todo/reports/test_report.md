# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260310_143343_todo\testing\tests`

## Return Code
1

## Stdout
```text
...F..F                                                                  [100%]
================================== FAILURES ===================================
______________________ test_module_wrapper_returns_dict _______________________

    def test_module_wrapper_returns_dict():
        module = importlib.import_module("generated_app.as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app")
        wrapper = getattr(module, "build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app")
>       result = wrapper({"sample": "payload"})
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

testing\tests\test_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app.py:14: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

payload = {'sample': 'payload'}

    def build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Function entrypoint used by generated tests and integration flows."""
>       todo_list_component, task_service, database = payload["components"]
                                                      ^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'components'

development\generated_app\as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app.py:53: KeyError
_______________________ test_generated_app_integration ________________________

    def test_generated_app_integration():
        result_1 = build_as_a_user_i_want_to_be_able_to_add_new_tasks_to_the_todo_app({'input': 'sample'})
        assert isinstance(result_1, dict)
        result_2 = build_as_a_user_i_want_to_be_able_to_mark_tasks_as_completed_in_the_to({'input': 'sample'})
        assert isinstance(result_2, dict)
>       result_3 = build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app({'input': 'sample'})
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

testing\tests\test_integration_generated_app.py:13: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

payload = {'input': 'sample'}

    def build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Function entrypoint used by generated tests and integration flows."""
>       todo_list_component, task_service, database = payload["components"]
                                                      ^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'components'

development\generated_app\as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app.py:53: KeyError
=========================== short test summary info ===========================
FAILED testing/tests/test_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app.py::test_module_wrapper_returns_dict
FAILED testing/tests/test_integration_generated_app.py::test_generated_app_integration
2 failed, 5 passed in 0.15s
```

## Stderr
```text

```
