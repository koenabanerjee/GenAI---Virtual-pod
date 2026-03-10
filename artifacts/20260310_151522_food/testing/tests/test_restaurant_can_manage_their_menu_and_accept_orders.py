"""Auto-generated unit tests for module restaurant_can_manage_their_menu_and_accept_orders."""

import importlib


def test_module_imports():
    module = importlib.import_module("generated_app.restaurant_can_manage_their_menu_and_accept_orders")
    assert module is not None


def test_module_wrapper_returns_dict():
    module = importlib.import_module("generated_app.restaurant_can_manage_their_menu_and_accept_orders")
    wrapper = getattr(module, "build_restaurant_can_manage_their_menu_and_accept_orders")
    result = wrapper({"sample": "payload"})
    assert isinstance(result, dict)
    assert "status" in result
