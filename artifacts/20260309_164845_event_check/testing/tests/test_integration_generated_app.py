"""Integration tests for generated modules."""

from generated_app.bakery_app_with_catalog_and_sales_reports import build_bakery_app_with_catalog_and_sales_reports


def test_generated_app_integration():
    result_1 = build_bakery_app_with_catalog_and_sales_reports({'input': 'sample'})
    assert isinstance(result_1, dict)
