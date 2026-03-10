"""Integration tests for generated modules."""

from generated_app.user_can_place_an_order_for_food_delivery import build_user_can_place_an_order_for_food_delivery
from generated_app.restaurant_can_manage_their_menu_and_accept_orders import build_restaurant_can_manage_their_menu_and_accept_orders
from generated_app.delivery_driver_can_manage_their_route_and_accept_orders import build_delivery_driver_can_manage_their_route_and_accept_orders


def test_generated_app_integration():
    result_1 = build_user_can_place_an_order_for_food_delivery({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_restaurant_can_manage_their_menu_and_accept_orders({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_delivery_driver_can_manage_their_route_and_accept_orders({'input': 'sample'})
    assert isinstance(result_3, dict)
