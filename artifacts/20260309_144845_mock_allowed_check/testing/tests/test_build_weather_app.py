"""Auto-generated unit tests for module build_weather_app."""

import importlib


def test_module_imports():
    module = importlib.import_module("generated_app.build_weather_app")
    assert module is not None


def test_module_wrapper_returns_dict():
    module = importlib.import_module("generated_app.build_weather_app")
    wrapper = getattr(module, "build_build_weather_app")
    result = wrapper({"sample": "payload"})
    assert isinstance(result, dict)
    assert "status" in result
