"""Integration tests for generated modules."""

from generated_app.create_a_virtual_dev_pod_that_writes_code_and_tests_from_require import build_create_a_virtual_dev_pod_that_writes_code_and_tests_from_require


def test_generated_app_integration():
    result_1 = build_create_a_virtual_dev_pod_that_writes_code_and_tests_from_require({'input': 'sample'})
    assert isinstance(result_1, dict)
