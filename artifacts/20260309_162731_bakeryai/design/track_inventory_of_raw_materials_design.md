# Software Design Specification for US-003: Track Inventory of Raw Materials

## 1. Component Scope

This component is designed to help bakery staff monitor and manage the inventory levels of raw materials. The system will provide current inventory levels and send alerts when inventory thresholds are reached.

### Components

- **Inventory Management System**: A web application where bakery staff can view and manage inventory levels.
- **Alerting System**: A notification system that sends alerts when inventory levels reach a certain threshold.

### Actors

- **Bakery Staff**: Users who interact with the Inventory Management System to view and manage inventory levels.

## 2. Architecture and Interfaces

![Inventory Management System Architecture Diagram](https://i.imgur.com/7LjX2jK.png)

### Interfaces

#### Inventory Management System (UI)

- **View Inventory**: Displays the current inventory levels of all raw materials.
- **Set Thresholds**: Allows bakery staff to set inventory level thresholds for each raw material.

#### Alerting System (API)

- **Receive Alerts**: Sends notifications to bakery staff when inventory levels reach a threshold.

## 3. Data Contracts

### Inventory

| Field          | Type   | Description                                                 |
| -------------- | ------ | ----------------------------------------------------------- |
| id             | int    | Unique identifier for each inventory record                |
| material_name   | string | Name of the raw material                                    |
| quantity        | int    | Current quantity of the raw material in stock               |
| reorder_threshold | int | Minimum quantity of the raw material before an alert is sent |

## 4. Risks and Mitigations

### Risks

- **Inaccurate Inventory Data**: Incorrect inventory data could lead to incorrect decisions being made.
- **Lack of Timely Alerts**: Delayed or missed alerts could result in stockouts or wastage.

### Mitigations

- **Regular Data Verification**: Implement data verification processes to ensure inventory data is accurate.
- **Reliable Alerting System**: Use a reliable alerting system to ensure timely notifications.

## 5. Non-functional considerations

### Performance

- The system should be able to handle a large number of inventory records without significant performance degradation.

### Security

- The system should implement appropriate security measures to protect inventory data from unauthorized access.

### Scalability

- The system should be designed to easily scale to accommodate future growth in the number of raw materials and bakery locations.