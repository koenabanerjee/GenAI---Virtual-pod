"""Integration tests for generated modules."""

from generated_app.as_a_user_i_want_to_be_able_to_add_new_tasks_to_the_todo_app import build_as_a_user_i_want_to_be_able_to_add_new_tasks_to_the_todo_app
from generated_app.as_a_user_i_want_to_be_able_to_mark_tasks_as_completed_in_the_to import build_as_a_user_i_want_to_be_able_to_mark_tasks_as_completed_in_the_to
from generated_app.as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app import build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app


def test_generated_app_integration():
    result_1 = build_as_a_user_i_want_to_be_able_to_add_new_tasks_to_the_todo_app({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_as_a_user_i_want_to_be_able_to_mark_tasks_as_completed_in_the_to({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app({'input': 'sample'})
    assert isinstance(result_3, dict)
