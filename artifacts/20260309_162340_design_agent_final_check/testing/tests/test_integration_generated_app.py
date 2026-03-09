"""Integration tests for generated modules."""

from generated_app.implement_notifications_for_severe_weather_alerts import build_implement_notifications_for_severe_weather_alerts


def test_generated_app_integration():
    result_1 = build_implement_notifications_for_severe_weather_alerts({'input': 'sample'})
    assert isinstance(result_1, dict)
