# Import required modules
from generated_app.process_customer_orders import build_process_customer_orders

def test_create_new_customer_order():
    # Given a new customer order with valid details
    customer_order = {
        "customer_name": "John Doe",
        "order_items": [
            {"item_name": "Cake", "quantity": 1},
            {"item_name": "Bread", "quantity": 2}
        ],
        "total_price": 25.5
    }

    # When processing the customer order
    processed_order = build_process_customer_orders(customer_order)

    # Then the processed order should have the same details as the original order
    assert processed_order == customer_order

def test_update_existing_customer_order():
    # Given an existing customer order with valid details
    customer_order = {
        "customer_name": "John Doe",
        "order_items": [
            {"item_name": "Cake", "quantity": 1},
            {"item_name": "Bread", "quantity": 2}
        ],
        "total_price": 25.5,
        "status": "pending"
    }

    # When updating the order status to completed
    customer_order["status"] = "completed"
    processed_order = build_process_customer_orders(customer_order)

    # Then the processed order should have the updated status
    assert processed_order["status"] == "completed"

def test_mark_order_as_completed():
    # Given an existing customer order with valid details and pending status
    customer_order = {
        "customer_name": "John Doe",
        "order_items": [
            {"item_name": "Cake", "quantity": 1},
            {"item_name": "Bread", "quantity": 2}
        ],
        "total_price": 25.5,
        "status": "pending"
    }

    # When processing the customer order to mark it as completed
    processed_order = build_process_customer_orders(customer_order)

    # Then the processed order should have the updated status
    assert processed_order["status"] == "completed"

def test_process_customer_orders_output_contract():
    # Given a customer order with valid details
    customer_order = {
        "customer_name": "John Doe",
        "order_items": [
            {"item_name": "Cake", "quantity": 1},
            {"item_name": "Bread", "quantity": 2}
        ],
        "total_price": 25.5
    }

    # When processing the customer order
    processed_order = build_process_customer_orders(customer_order)

    # Then the processed order should have the same structure as the expected output contract
    expected_output = {
        "customer_name": "John Doe",
        "order_items": [
            {"item_name": "Cake", "quantity": 1},
            {"item_name": "Bread", "quantity": 2}
        ],
        "total_price": 25.5,
        "status": "pending"
    }

    assert processed_order.keys() == expected_output.keys()
    for key in expected_output:
        assert isinstance(processed_order[key], (str, list, float))
