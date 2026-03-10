# Test Execution Report

## Command
`C:\Python313\python.exe -m pytest -q C:\Users\Koena\OneDrive\Desktop\GenAI\artifacts\20260310_151522_food\testing\tests`

## Return Code
1

## Stdout
```text
.FF.F.F                                                                  [100%]
================================== FAILURES ===================================
______________________ test_module_wrapper_returns_dict _______________________

    def test_module_wrapper_returns_dict():
        module = importlib.import_module("generated_app.delivery_driver_can_manage_their_route_and_accept_orders")
        wrapper = getattr(module, "build_delivery_driver_can_manage_their_route_and_accept_orders")
>       result = wrapper({"sample": "payload"})
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

testing\tests\test_delivery_driver_can_manage_their_route_and_accept_orders.py:14: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

payload = {'sample': 'payload'}

    def build_delivery_driver_can_manage_their_route_and_accept_orders(payload: Dict[str, Any]) -> Dict[str, Any]:
        """Function entrypoint used by generated tests and integration flows."""
>       service = DeliveryDriverCanManageTheirRouteAndAcceptOrdersService(payload["base_url"])
                                                                          ^^^^^^^^^^^^^^^^^^^
E       KeyError: 'base_url'

development\generated_app\delivery_driver_can_manage_their_route_and_accept_orders.py:72: KeyError
_______________________ test_generated_app_integration ________________________

    def test_generated_app_integration():
>       result_1 = build_user_can_place_an_order_for_food_delivery({'input': 'sample'})
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

testing\tests\test_integration_generated_app.py:9: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
development\generated_app\user_can_place_an_order_for_food_delivery.py:48: in build_user_can_place_an_order_for_food_delivery
    return UserCanPlaceAnOrderForFoodDeliveryService().execute(payload)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = UserCanPlaceAnOrderForFoodDeliveryService()
payload = {'input': 'sample'}

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
>       food_options = payload["food_options"]  # Fetch food options from the backend API
                       ^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'food_options'

development\generated_app\user_can_place_an_order_for_food_delivery.py:12: KeyError
______________________ test_module_wrapper_returns_dict _______________________

    def test_module_wrapper_returns_dict():
        module = importlib.import_module("generated_app.restaurant_can_manage_their_menu_and_accept_orders")
        wrapper = getattr(module, "build_restaurant_can_manage_their_menu_and_accept_orders")
        result = wrapper({"sample": "payload"})
>       assert isinstance(result, dict)
E       assert False
E        +  where False = isinstance(None, dict)

testing\tests\test_restaurant_can_manage_their_menu_and_accept_orders.py:15: AssertionError
______________________ test_module_wrapper_returns_dict _______________________

    def test_module_wrapper_returns_dict():
        module = importlib.import_module("generated_app.user_can_place_an_order_for_food_delivery")
        wrapper = getattr(module, "build_user_can_place_an_order_for_food_delivery")
>       result = wrapper({"sample": "payload"})
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

testing\tests\test_user_can_place_an_order_for_food_delivery.py:14: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
development\generated_app\user_can_place_an_order_for_food_delivery.py:48: in build_user_can_place_an_order_for_food_delivery
    return UserCanPlaceAnOrderForFoodDeliveryService().execute(payload)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = UserCanPlaceAnOrderForFoodDeliveryService()
payload = {'sample': 'payload'}

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
>       food_options = payload["food_options"]  # Fetch food options from the backend API
                       ^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'food_options'

development\generated_app\user_can_place_an_order_for_food_delivery.py:12: KeyError
=========================== short test summary info ===========================
FAILED testing/tests/test_delivery_driver_can_manage_their_route_and_accept_orders.py::test_module_wrapper_returns_dict
FAILED testing/tests/test_integration_generated_app.py::test_generated_app_integration
FAILED testing/tests/test_restaurant_can_manage_their_menu_and_accept_orders.py::test_module_wrapper_returns_dict
FAILED testing/tests/test_user_can_place_an_order_for_food_delivery.py::test_module_wrapper_returns_dict
4 failed, 3 passed in 0.21s
```

## Stderr
```text

```
