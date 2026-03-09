"""Integration tests for generated modules."""

from generated_app.develop_a_feature_to_analyze_student_data_for_performance_predic import build_develop_a_feature_to_analyze_student_data_for_performance_predic
from generated_app.create_a_user_interface_for_teachers_to_view_student_performance import build_create_a_user_interface_for_teachers_to_view_student_performance
from generated_app.implement_data_visualization_tools_to_help_teachers_understand_s import build_implement_data_visualization_tools_to_help_teachers_understand_s


def test_generated_app_integration():
    result_1 = build_develop_a_feature_to_analyze_student_data_for_performance_predic({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_create_a_user_interface_for_teachers_to_view_student_performance({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_implement_data_visualization_tools_to_help_teachers_understand_s({'input': 'sample'})
    assert isinstance(result_3, dict)
