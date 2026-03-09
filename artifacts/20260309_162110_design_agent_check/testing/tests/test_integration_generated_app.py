"""Integration tests for generated modules."""

from generated_app.ai_based_weather_app_with_hourly_updates import build_ai_based_weather_app_with_hourly_updates


def test_generated_app_integration():
    result_1 = build_ai_based_weather_app_with_hourly_updates({'input': 'sample'})
    assert isinstance(result_1, dict)
