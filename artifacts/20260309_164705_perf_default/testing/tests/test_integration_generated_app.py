"""Integration tests for generated modules."""

from generated_app.build_bakery_ai_with_sales_and_catalog import build_build_bakery_ai_with_sales_and_catalog


def test_generated_app_integration():
    result_1 = build_build_bakery_ai_with_sales_and_catalog({'input': 'sample'})
    assert isinstance(result_1, dict)
