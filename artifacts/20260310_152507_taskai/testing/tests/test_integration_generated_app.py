"""Integration tests for generated modules."""

from generated_app.as_a_project_manager_i_want_to_create_a_new_project_in_the_team import build_as_a_project_manager_i_want_to_create_a_new_project_in_the_team
from generated_app.as_a_team_member_i_want_to_be_able_to_view_and_manage_my_assigne import build_as_a_team_member_i_want_to_be_able_to_view_and_manage_my_assigne
from generated_app.as_a_project_manager_i_want_to_export_project_reports_to_pdf_and import build_as_a_project_manager_i_want_to_export_project_reports_to_pdf_and


def test_generated_app_integration():
    result_1 = build_as_a_project_manager_i_want_to_create_a_new_project_in_the_team({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_as_a_team_member_i_want_to_be_able_to_view_and_manage_my_assigne({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_as_a_project_manager_i_want_to_export_project_reports_to_pdf_and({'input': 'sample'})
    assert isinstance(result_3, dict)
