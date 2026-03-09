"""Auto-generated module for US-001: Manage Product Catalog."""

from __future__ import annotations
from typing import Any, Dict

import requests

@dataclass
class ManageProductCatalogService:
    """Implementation class aligned to user story US-001."""

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        product_data = payload["product"]

        url = "http://bakery-management-system:8000/api/v1"

        if "action" not in product_data or product_data["action"] not in ["add", "edit", "delete"]:
            return {
                "story_id": self.story_id,
                "status": "failed",
                "input": payload,
                "summary": "Invalid request. Please provide a valid 'action' and 'product' data.",
                "acceptance": "As a bakery staff member, I can add, edit, or delete a product with a valid 'action' and 'product' data.",
            }

        if product_data["action"] == "add":
            response = requests.post(url + "/products", json=product_data)

            if response.status_code != 201:
                return {
                    "story_id": self.story_id,
                    "status": "failed",
                    "input": payload,
                    "summary": f"Failed to add product. Status code: {response.status_code}",
                    "acceptance": "As a bakery staff member, I can add a new product to the catalog with all necessary details.",
                }

            product_id = response.json()["id"]
            return {
                "story_id": self.story_id,
                "status": "success",
                "input": payload,
                "summary": f"Product with id {product_id} added successfully.",
                "acceptance": "As a bakery staff member, I can add a new product to the catalog with all necessary details.",
            }

        if product_data["action"] == "edit":
            product_id = product_data["id"]
            response = requests.put(url + f"/products/{product_id}", json=product_data)

            if response.status_code != 200:
                return {
                    "story_id": self.story_id,
                    "status": "failed",
                    "input": payload,
                    "summary": f"Failed to edit product with id {product_id}. Status code: {response.status_code}",
                    "acceptance": "As a bakery staff member, I can edit an existing product's details.",
                }

            return {
                "story_id": self.story_id,
                "status": "success",
                "input": payload,
                "summary": f"Product with id {product_id} edited successfully.",
                "acceptance": "As a bakery staff member, I can edit an existing product's details.",
            }

        if product_data["action"] == "delete":
            product_id = product_data["id"]
            response = requests.delete(url + f"/products/{product_id}")

            if response.status_code != 204:
                return {
                    "story_id": self.story_id,
                    "status": "failed",
                    "input": payload,
                    "summary": f"Failed to delete product with id {product_id}. Status code: {response.status_code}",
                    "acceptance": "As a bakery staff member, I can delete a product from the catalog.",
                }

            return {
                "story_id": self.story_id,
                "status": "success",
                "input": payload,
                "summary": f"Product with id {product_id} deleted successfully.",
                "acceptance": "As a bakery staff member, I can delete a product from the catalog.",
            }

def build_manage_product_catalog(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    manage_product_catalog_service = ManageProductCatalogService()
    return manage_product_catalog_service.execute(payload)
