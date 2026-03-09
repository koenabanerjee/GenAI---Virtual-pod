import pytest
from generated_app import manage_product_catalog as mpc, process_customer_orders as pco, \
    track_inventory_of_raw_materials as tirm, generate_sales_reports as gsr, \
    manage_suppliers_and_employees as mse

def test_generated_app_integration():
    # Test manage_product_catalog
    result_mpc = mpc.build_manage_product_catalog()
    assert result_mpc is not None
    assert "story_id" in result_mpc and "status" in result_mpc

    # Test process_customer_orders
    result_pco = pco.build_process_customer_orders()
    assert result_pco is not None
    assert "story_id" in result_pco and "status" in result_pco

    # Test track_inventory_of_raw_materials
    result_tirm = tirm.build_track_inventory_of_raw_materials()
    assert result_tirm is not None
    assert "story_id" in result_tirm and "status" in result_tirm

    # Test generate_sales_reports
    result_gsr = gsr.build_generate_sales_reports()
    assert result_gsr is not None
    assert "story_id" in result_gsr and "status" in result_gsr

    # Test manage_suppliers_and_employees
    result_mse = mse.build_manage_suppliers_and_employees()
    assert result_mse is not None
    assert "story_id" in result_mse and "status" in result_mse
