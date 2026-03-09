"""Integration tests for generated modules."""

from generated_app.build_weather_app import build_build_weather_app


def test_generated_app_integration():
    result_1 = build_build_weather_app({'input': 'sample'})
    assert isinstance(result_1, dict)
