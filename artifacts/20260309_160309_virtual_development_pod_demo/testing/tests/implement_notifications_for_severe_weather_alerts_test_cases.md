# Test Case Document - US-005: Implement notifications for severe weather alerts

## 1. Objective
The objective of this test case document is to validate the functionality of the severe weather alert notifications feature as described in the US-005 story. The feature should be able to fetch severe weather alerts from reliable sources, provide real-time notifications, allow users to customize notification preferences, and offer options to snooze or dismiss notifications.

## 2. Preconditions
- The app is installed and running on a compatible device.
- The user has an active internet connection.
- The user has granted the necessary permissions for location services and notifications.

## 3. Test Cases

### Fetching Severe Weather Alerts
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC-001 | Verify that the app fetches severe weather alerts from reliable sources. | The app should display accurate and up-to-date severe weather alerts. |
| TC-002 | Verify that the app fetches alerts for various weather conditions, such as heavy rain, thunderstorms, tornadoes, and hurricanes. | The app should display alerts for all the mentioned weather conditions. |

### Real-time Notifications
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC-003 | Verify that the app provides real-time notifications for severe weather alerts. | The app should display a notification as soon as a new severe weather alert is available. |
| TC-004 | Verify that the app does not send duplicate notifications for the same alert. | The app should only send one notification for each severe weather alert. |

### Customizing Notification Preferences
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC-005 | Verify that users can customize notification preferences. | Users should be able to choose which types of severe weather alerts they want to receive notifications for. |
| TC-006 | Verify that users can choose the notification sound and vibration settings. | Users should be able to select their preferred notification sound and vibration intensity. |

### Snooze or Dismiss Notifications
| Test Case ID | Description | Expected Result |
| --- | --- | --- |
| TC-007 | Verify that users can snooze notifications. | Users should be able to snooze notifications for a specified duration, after which they will be displayed again. |
| TC-008 | Verify that users can dismiss notifications. | Users should be able to dismiss notifications permanently, preventing them from being displayed again. |

## 4. Exit Criteria
- All test cases pass without any errors or exceptions.
- The app functions correctly and meets the acceptance criteria for US-005.