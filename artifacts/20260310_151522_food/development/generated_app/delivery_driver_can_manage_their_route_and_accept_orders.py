"""Auto-generated module for US-003: Delivery Driver can manage their route and accept orders."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict
import requests

@dataclass
class DeliveryDriverCanManageTheirRouteAndAcceptOrdersService:
    """Implementation class aligned to user story US-003."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Allows delivery drivers to manage their route and accept orders",
            "acceptance": {
                "Driver can view their current route and upcoming orders": self.view_route_and_orders,
                "Driver can accept or decline orders": self.accept_or_decline_orders,
                "Driver can navigate to the delivery location using the app": self.navigate_to_delivery_location,
                "Driver can update order status in real-time": self.update_order_status,
                "Driver can communicate with the user regarding estimated delivery time": self.communicate_with_user,
            },
        }
        return result

    def view_route_and_orders(self, driver_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/drivers/{driver_id}/route"
        response = requests.get(url)
        return response.json()

    def accept_or_decline_orders(self, driver_id: str, order_id: str, accept: bool) -> Dict[str, Any]:
        url = f"{self.base_url}/drivers/{driver_id}/orders/{order_id}/{accept}"
        response = requests.put(url)
        return response.json()

    def navigate_to_delivery_location(self, driver_id: str, order_id: str) -> Dict[str, Any]:
        order = self.get_order(driver_id, order_id)
        navigation_system_url = order["navigation_system_url"]
        location_data = {
            "pickup_location": order["pickup_location"],
            "delivery_location": order["delivery_location"],
        }
        response = requests.post(navigation_system_url, json=location_data)
        return response.json()

    def update_order_status(self, driver_id: str, order_id: str, status: str) -> Dict[str, Any]:
        url = f"{self.base_url}/drivers/{driver_id}/orders/{order_id}/status"
        response = requests.put(url, json={"status": status})
        return response.json()

    def communicate_with_user(self, driver_id: str, order_id: str, message: str) -> Dict[str, Any]:
        url = f"{self.base_url}/drivers/{driver_id}/messages"
        data = {"recipient": "user", "content": message}
        response = requests.post(url, json=data)
        order = self.get_order(driver_id, order_id)
        order["last_message"] = response.json()
        return {"order": order}

    def get_order(self, driver_id: str, order_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/drivers/{driver_id}/orders/{order_id}"
        response = requests.get(url)
        return response.json()


def build_delivery_driver_can_manage_their_route_and_accept_orders(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    service = DeliveryDriverCanManageTheirRouteAndAcceptOrdersService(payload["base_url"])
    return service.execute(payload)
