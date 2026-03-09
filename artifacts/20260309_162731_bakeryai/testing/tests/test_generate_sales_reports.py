import pytest
from generated_app import generate_sales_reports

def test_import():
    """Test if the generate_sales_reports module can be imported."""
    assert generate_sales_reports is not None

def test_daily_sales_report():
    """Test generating a daily sales report."""
    daily_sales = generate_sales_reports.build_generate_sales_reports("daily")
    assert isinstance(daily_sales, list)
    assert len(daily_sales) > 0

def test_weekly_sales_report():
    """Test generating a weekly sales report."""
    weekly_sales = generate_sales_reports.build_generate_sales_reports("weekly")
    assert isinstance(weekly_sales, list)
    assert len(weekly_sales) > 0

def test_monthly_sales_report():
    """Test generating a monthly sales report."""
    monthly_sales = generate_sales_reports.build_generate_sales_reports("monthly")
    assert isinstance(monthly_sales, list)
    assert len(monthly_sales) > 0

def test_sales_report_data():
    """Test sales report data."""
    daily_sales = generate_sales_reports.build_generate_sales_reports("daily")[0]
    weekly_sales = generate_sales_reports.build_generate_sales_reports("weekly")[0]
    monthly_sales = generate_sales_reports.build_generate_sales_reports("monthly")[0]

    assert "date" in daily_sales
    assert "total_sales" in daily_sales
    assert "weekly_sales" in weekly_sales
    assert "monthly_sales" in monthly_sales

    assert isinstance(daily_sales["date"], str)
    assert isinstance(daily_sales["total_sales"], float)
    assert isinstance(weekly_sales["weekly_sales"], list)
    assert isinstance(weekly_sales["monthly_sales"], list)

    for sale in weekly_sales["weekly_sales"]:
        assert isinstance(sale["date"], str)
        assert isinstance(sale["total_sales"], float)

    for sale in monthly_sales["monthly_sales"]:
        assert isinstance(sale["date"], str)
        assert isinstance(sale["total_sales"], float)
