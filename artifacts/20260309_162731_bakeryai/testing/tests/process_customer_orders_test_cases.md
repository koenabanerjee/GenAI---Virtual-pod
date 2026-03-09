# Test Case Document - US-002: Process Customer Orders

## 1. Objective
The objective of this test case document is to verify the functionality of the `process_customer_orders` module in the bakery system, specifically the ability for a bakery staff member to create a new customer order, update an existing customer order, and mark an order as completed.

## 2. Preconditions
- The bakery system is up and running.
- The staff member has logged in to the system with valid credentials.
- The necessary customer and product data are available in the system.

## 3. Test Cases

### Creating a New Customer Order
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC001 | Staff member navigates to the customer orders page and clicks on "New Order" button | A new order form is displayed |
| TC002 | Staff member enters valid customer details and selects desired products | The order is created with the entered details and selected products |
| TC003 | Staff member saves the order | The order is saved and displayed in the list of orders |
| TC004 | Staff member verifies that the order is associated with the correct customer | The order is displayed under the correct customer's name in the list of orders |

### Updating an Existing Customer Order
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC011 | Staff member navigates to an existing order and clicks on the "Edit" button | The order form is displayed with the existing data pre-populated |
| TC012 | Staff member updates any of the order details (customer name, products, etc.) | The updated details are saved and displayed in the order form and list of orders |
| TC013 | Staff member saves the updated order | The order is updated and displayed in the list of orders with the new details |

### Marking an Order as Completed
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC021 | Staff member navigates to an existing order and clicks on the "Mark as Completed" button | The order status is updated to "Completed" |
| TC022 | Staff member verifies that the order status is displayed as "Completed" in the list of orders | The order status is displayed as "Completed" in the list of orders |
| TC023 | Staff member is unable to make further updates to the completed order | The order is no longer editable and the "Edit" button is disabled |

## 4. Exit Criteria
- All test cases have been executed and passed.
- The `process_customer_orders` module functions as expected for creating, updating, and marking orders as completed.