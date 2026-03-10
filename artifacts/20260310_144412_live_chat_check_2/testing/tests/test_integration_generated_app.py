"""Integration tests for generated modules."""

from generated_app.build_a_todo_app_with_add_complete_delete_tasks_and_reports import build_build_a_todo_app_with_add_complete_delete_tasks_and_reports


def test_generated_app_integration():
    result_1 = build_build_a_todo_app_with_add_complete_delete_tasks_and_reports({'input': 'sample'})
    assert isinstance(result_1, dict)
