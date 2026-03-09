# Test Case Document - US-003: Track Inventory of Raw Materials

## 1. Objective
The objective of this test case is to verify that the bakery staff can view the current inventory levels of raw materials and receive alerts when inventory levels reach a certain threshold in the `track_inventory_of_raw_materials` module.

## 2. Preconditions
- The `track_inventory_of_raw_materials` module is properly installed and configured.
- The bakery staff member has valid login credentials.
- The raw materials inventory data is available and accurate in the system.

## 3. Test Cases

### View Current Inventory Levels
| **Test Case ID** | **Test Case Description** | **Expected Result** |
| --- | --- | --- |
| TVC-001 | Verify that the bakery staff member can view the current inventory levels of raw materials | The system displays the current inventory levels of all raw materials. |
| TVC-002 | Verify that the bakery staff member can filter the inventory levels by raw material type | The system allows the staff member to filter the inventory levels by raw material type and displays the current inventory levels for each type. |

### Receive Alerts
| **Test Case ID** | **Test Case Description** | **Expected Result** |
| --- | --- | --- |
| TA-001 | Verify that the bakery staff member receives an alert when inventory level of a raw material reaches a certain threshold | The system sends an alert to the staff member via email or notification when the inventory level of a raw material reaches a predefined threshold. |
| TA-002 | Verify that the bakery staff member can acknowledge and dismiss the alert | The system allows the staff member to acknowledge and dismiss the alert. |
| TA-003 | Verify that the alert is displayed in the system interface | The system displays the alert in the interface until it is acknowledged by the staff member. |

## 4. Exit Criteria
- All test cases have passed.
- The bakery staff member can view the current inventory levels of raw materials and receive alerts when inventory levels reach a certain threshold.