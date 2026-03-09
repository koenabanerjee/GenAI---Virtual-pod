# US-004: Generate Sales Reports

## Objective
The objective of this test case is to verify that the bakery manager can generate daily, weekly, and monthly sales reports using the `generate_sales_reports` module.

## Preconditions
- The system is logged in with valid bakery manager credentials.
- The sales data for the desired report period is available in the system.

## Test Cases

### Test Case 1: Generate Daily Sales Report
1. Log in to the system with valid bakery manager credentials.
2. Navigate to the `generate_sales_reports` module.
3. Select the "Daily" report option.
4. Enter the desired start and end date for the report.
5. Click the "Generate Report" button.
6. Verify that the system generates and displays the daily sales report.
7. Verify that the report contains the correct sales data for the selected date range.

### Test Case 2: Generate Weekly Sales Report
1. Log in to the system with valid bakery manager credentials.
2. Navigate to the `generate_sales_reports` module.
3. Select the "Weekly" report option.
4. Enter the start and end date for the report week (Sunday to Saturday).
5. Click the "Generate Report" button.
6. Verify that the system generates and displays the weekly sales report.
7. Verify that the report contains the correct sales data for the selected week.

### Test Case 3: Generate Monthly Sales Report
1. Log in to the system with valid bakery manager credentials.
2. Navigate to the `generate_sales_reports` module.
3. Select the "Monthly" report option.
4. Enter the start and end date for the report month.
5. Click the "Generate Report" button.
6. Verify that the system generates and displays the monthly sales report.
7. Verify that the report contains the correct sales data for the selected month.

## Exit Criteria
- The bakery manager can generate daily, weekly, and monthly sales reports.
- The generated reports contain the correct sales data for the selected period.
- The system displays the generated reports without errors.