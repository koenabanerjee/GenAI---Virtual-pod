"""Auto-generated unit tests for module as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app."""

import importlib


def test_module_imports():
    module = importlib.import_module("generated_app.as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app")
    assert module is not None


def test_module_wrapper_returns_dict():
    module = importlib.import_module("generated_app.as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app")
    wrapper = getattr(module, "build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app")
    result = wrapper({"sample": "payload"})
    assert isinstance(result, dict)
    assert "status" in result
