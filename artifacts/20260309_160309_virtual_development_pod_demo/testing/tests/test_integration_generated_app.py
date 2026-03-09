import pytest
from ai_based_weather_app_with_hourly_updates import build_app as ai_app_builder
from integration_of_external_weather_data_sources import build_integration as data_integration_builder
from implement_machine_learning_model_for_weather_prediction import build_model as ml_model_builder
from design_and_develop_user_interface_for_hourly_weather_forecasts import build_ui as ui_builder
from implement_notifications_for_severe_weather_alerts import build_notifications as alert_builder

def test_generated_app_integration():
    # Build each module
    app = ai_app_builder()
    data_integration = data_integration_builder()
    ml_model = ml_model_builder()
    ui = ui_builder()
    notifications = alert_builder()

    # Validate each call returns a dict with keys 'story_id' and 'status'
    assert isinstance(app, dict) and 'story_id' in app and 'status' in app
    assert isinstance(data_integration, dict) and 'story_id' in data_integration and 'status' in data_integration
    assert isinstance(ml_model, dict) and 'story_id' in ml_model and 'status' in ml_model
    assert isinstance(ui, dict) and 'story_id' in ui and 'status' in ui
    assert isinstance(notifications, dict) and 'story_id' in notifications and 'status' in notifications
