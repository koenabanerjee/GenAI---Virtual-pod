# Test Case Document - US-005: Manage Suppliers and Employees

## 1. Objective
The objective of this test case document is to validate the functionality of managing suppliers and employees in the `manage_suppliers_and_employees` module.

## 2. Preconditions
- The `manage_suppliers_and_employees` module is accessible to the bakery manager.
- The system has internet connectivity.
- The bakery manager is logged in to the system with valid credentials.

## 3. Test Cases

### Adding a New Supplier
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC001 | Enter valid supplier details and click 'Add Supplier' button | Supplier is added to the system with success message |
| TC002 | Enter invalid supplier details and click 'Add Supplier' button | Error message is displayed and supplier is not added |
| TC003 | Add a supplier with existing name | Error message is displayed and supplier is not added |

### Editing an Existing Supplier
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC004 | Edit a supplier's details and click 'Update Supplier' button | Supplier details are updated with success message |
| TC005 | Edit a supplier's details with invalid information and click 'Update Supplier' button | Error message is displayed and supplier details are not updated |

### Deleting a Supplier
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC006 | Select a supplier and click 'Delete Supplier' button | Supplier is deleted with success message |
| TC007 | Try to delete a supplier with no records associated | Error message is displayed and supplier is not deleted |

### Adding a New Employee
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC008 | Enter valid employee details and click 'Add Employee' button | Employee is added to the system with success message |
| TC009 | Enter invalid employee details and click 'Add Employee' button | Error message is displayed and employee is not added |
| TC010 | Add an employee with existing name | Error message is displayed and employee is not added |

### Editing an Existing Employee
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC011 | Edit an employee's details and click 'Update Employee' button | Employee details are updated with success message |
| TC012 | Edit an employee's details with invalid information and click 'Update Employee' button | Error message is displayed and employee details are not updated |

### Deleting an Employee
| Test Case ID | Test Case Description | Expected Result |
| --- | --- | --- |
| TC013 | Select an employee and click 'Delete Employee' button | Employee is deleted with success message |
| TC014 | Try to delete an employee with no records associated | Error message is displayed and employee is not deleted |

## 4. Exit Criteria
- All test cases pass with expected results.
- No new bugs or defects are identified during testing.
- The functionality of managing suppliers and employees is validated and meets the acceptance criteria.