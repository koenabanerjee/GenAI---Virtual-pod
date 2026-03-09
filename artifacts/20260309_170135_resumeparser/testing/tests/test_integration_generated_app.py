"""Integration tests for generated modules."""

from generated_app.automate_resume_data_extraction_and_organization import build_automate_resume_data_extraction_and_organization
from generated_app.convert_unstructured_resume_data_into_structured_data import build_convert_unstructured_resume_data_into_structured_data
from generated_app.enable_quick_search_filter_and_evaluation_of_candidates import build_enable_quick_search_filter_and_evaluation_of_candidates


def test_generated_app_integration():
    result_1 = build_automate_resume_data_extraction_and_organization({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_convert_unstructured_resume_data_into_structured_data({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_enable_quick_search_filter_and_evaluation_of_candidates({'input': 'sample'})
    assert isinstance(result_3, dict)
