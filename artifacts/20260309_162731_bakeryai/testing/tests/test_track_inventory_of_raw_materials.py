import pytest
from generated_app.track_inventory_of_raw_materials import build_track_inventory_of_raw_materials

def test_import_track_inventory_of_raw_materials():
    """Test that the track_inventory_of_raw_materials module can be imported."""
    from generated_app.track_inventory_of_raw_materials import build_track_inventory_of_raw_materials

    assert build_track_inventory_of_raw_materials is not None

def test_build_track_inventory_of_raw_materials_output_contract():
    """Test that the output of build_track_inventory_of_raw_materials matches the expected contract."""
    expected_output = {
        "raw_materials": [],
        "threshold_levels": {},
        "current_inventory_levels": {}
    }

    output = build_track_inventory_of_raw_materials()

    assert output is not None
    assert isinstance(output, dict)
    assert set(output.keys()) == {"raw_materials", "threshold_levels", "current_inventory_levels"}
    assert all(isinstance(item, list) or isinstance(item, dict) for item in output.values())

def test_view_current_inventory_levels():
    """Test that the current inventory levels can be viewed."""
    raw_materials = ["flour", "sugar", "eggs"]
    threshold_levels = {"flour": 10, "sugar": 5, "eggs": 20}
    current_inventory_levels = {"flour": 8, "sugar": 7, "eggs": 15}

    output = build_track_inventory_of_raw_materials(raw_materials, threshold_levels)
    output["current_inventory_levels"] = current_inventory_levels

    assert output["current_inventory_levels"] == current_inventory_levels

def test_receive_alert_when_inventory_levels_reach_threshold():
    """Test that alerts are received when inventory levels reach a certain threshold."""
    raw_materials = ["flour", "sugar", "eggs"]
    threshold_levels = {"flour": 10, "sugar": 5, "eggs": 20}
    current_inventory_levels = {"flour": 8, "sugar": 4, "eggs": 18}

    output = build_track_inventory_of_raw_materials(raw_materials, threshold_levels)
    output["current_inventory_levels"] = current_inventory_levels

    alerts = output["alerts"]

    expected_alerts = {
        "flour": "Alert: Current inventory level of flour (8) is below the threshold level (10)",
        "sugar": "Alert: Current inventory level of sugar (4) is below the threshold level (5)"
    }

    assert alerts == expected_alerts
