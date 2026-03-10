"""Integration tests for generated modules."""

from generated_app.build_todo_app_with_add_and_complete import build_build_todo_app_with_add_and_complete


def test_generated_app_integration():
    result_1 = build_build_todo_app_with_add_and_complete({'input': 'sample'})
    assert isinstance(result_1, dict)
