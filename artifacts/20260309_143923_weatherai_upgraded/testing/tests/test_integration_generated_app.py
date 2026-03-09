"""Integration tests for generated modules."""

from generated_app.build_a_weather_prediction_system_with_data_ingestion_forecast_a import build_build_a_weather_prediction_system_with_data_ingestion_forecast_a


def test_generated_app_integration():
    result_1 = build_build_a_weather_prediction_system_with_data_ingestion_forecast_a({'input': 'sample'})
    assert isinstance(result_1, dict)
