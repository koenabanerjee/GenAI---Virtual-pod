"""Integration tests for generated modules."""

from generated_app.need_ba_dev_qa_pm_flow_with_reports import build_need_ba_dev_qa_pm_flow_with_reports


def test_generated_app_integration():
    result_1 = build_need_ba_dev_qa_pm_flow_with_reports({'input': 'sample'})
    assert isinstance(result_1, dict)
