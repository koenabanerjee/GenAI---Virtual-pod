"""Integration tests for generated modules."""

from generated_app.build_todo_app_with_add_complete_delete import build_build_todo_app_with_add_complete_delete


def test_generated_app_integration():
    result_1 = build_build_todo_app_with_add_complete_delete({'input': 'sample'})
    assert isinstance(result_1, dict)
