import pytest
from generated_app.manage_suppliers_and_employees import build_manage_suppliers_and_employees
from generated_app.manage_suppliers_and_employees.models import Supplier, Employee

@pytest.fixture
def initial_data():
    supplier = Supplier(id=1, name="Supplier A", contact="1234567890", address="123 Main St")
    employee = Employee(id=1, name="Employee A", position="Baker", salary=3000)
    yield (supplier, employee)
    Supplier.delete.call(supplier)
    Employee.delete.call(employee)

def test_build_manage_suppliers_and_employees_returns_correct_type():
    assert isinstance(build_manage_suppliers_and_employees(), ModuleType)

def test_add_new_supplier(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    new_supplier = Supplier(name="Supplier B", contact="0987654321", address="456 Elm St")
    manage_suppliers_and_employees.add_supplier(new_supplier)
    suppliers = manage_suppliers_and_employees.get_suppliers()
    assert len(suppliers) == 2
    assert new_supplier in suppliers

def test_edit_existing_supplier_information(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    initial_supplier = initial_data[0]
    new_contact = "5555555555"
    manage_suppliers_and_employees.edit_supplier(initial_supplier.id, new_contact)
    suppliers = manage_suppliers_and_employees.get_suppliers()
    assert len(suppliers) == 1
    assert initial_supplier.contact != suppliers[0].contact
    assert suppliers[0].contact == new_contact

def test_delete_supplier(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    manage_suppliers_and_employees.delete_supplier(initial_data[0].id)
    suppliers = manage_suppliers_and_employees.get_suppliers()
    assert len(suppliers) == 0

def test_add_new_employee(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    new_employee = Employee(name="Employee C", position="Decorator", salary=2500)
    manage_suppliers_and_employees.add_employee(new_employee)
    employees = manage_suppliers_and_employees.get_employees()
    assert len(employees) == 2
    assert new_employee in employees

def test_edit_existing_employee_information(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    initial_employee = initial_data[1]
    new_position = "Cake Decorator"
    manage_suppliers_and_employees.edit_employee(initial_employee.id, new_position)
    employees = manage_suppliers_and_employees.get_employees()
    assert len(employees) == 1
    assert initial_employee.position != employees[0].position
    assert employees[0].position == new_position

def test_delete_employee(initial_data):
    manage_suppliers_and_employees = build_manage_suppliers_and_employees()
    manage_suppliers_and_employees.delete_employee(initial_data[1].id)
    employees = manage_suppliers_and_employees.get_employees()
    assert len(employees) == 0
