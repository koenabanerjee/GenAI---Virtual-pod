"""Auto-generated module for US-003: Track Inventory of Raw Materials."""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class Inventory:
 """Represents an inventory record."""

 inventory_id: int
 material_name: str
 quantity: int
 reorder_threshold: int

@dataclass
class InventoryService:
 """Service to manage inventory records."""

 inventory_records: List[Inventory]

 def __init__(self, inventory_records: List[Inventory] = []):
 """Initialize InventoryService with an optional list of inventory records."""
 self.inventory_records = inventory_records

 def add_inventory(self, inventory: Inventory):
 """Add a new inventory record."""
 self.inventory_records.append(inventory)

 def get_current_inventory(self):
 """Return the current inventory levels of all raw materials."""
 return {material.material_name: material.quantity for material in self.inventory_records}

 def set_threshold(self, material_name: str, threshold: int):
 """Set the reorder threshold for a raw material."""
 for inventory in self.inventory_records:
 if inventory.material_name == material_name:
 inventory.reorder_threshold = threshold

 @dataclass
class AlertService:
 """Service to manage alerts."""

 def __init__(self):
 self.alerts: List[str] = []

 def send_alert(self, message: str):
 """Send an alert to bakery staff."""
 self.alerts.append(message)

@dataclass
class TrackInventoryOfRawMaterialsService:
 """Service to track inventory levels of raw materials."""

 inventory_service: InventoryService
 alert_service: AlertService

 def __init__(self, inventory_records: List[Inventory] = []):
 self.inventory_service = InventoryService(inventory_records)
 self.alert_service = AlertService()

 def build_track_inventory_of_raw_materials(self, payload: Dict[str, Any]) -> Dict[str, Any]:
 inventory = self.inventory_service.get_current_inventory()
 for material, quantity in inventory.items():
 if quantity <= material.reorder_threshold:
 self.alert_service.send_alert(f"Low inventory: {material} ({quantity} left)")

 result = {
 "story_id": self.story_id,
 "status": "implemented",
 "input": payload,
 "summary": "As a bakery staff member, I can view the current inventory levels of raw materials and receive alerts when inventory levels reach a certain threshold.",
 "acceptance": {
 "Given": "I am a bakery staff member.",
 "When": "I access the Inventory Management System.",
 "Then": "I can view the current inventory levels of all raw materials.",
 "And": "I can set inventory level thresholds for each raw material.",
 "When": "Inventory levels reach a threshold.",
 "Then": "I receive an alert."
 }
 }
 return result

def build_track_inventory_of_raw_materials_service(inventory_records: List[Inventory] = []):
 """Function entrypoint used by generated tests and integration flows."""
 track_inventory_service = TrackInventoryOfRawMaterialsService(inventory_records)
 return track_inventory_service.build_track_inventory_of_raw_materials({})
