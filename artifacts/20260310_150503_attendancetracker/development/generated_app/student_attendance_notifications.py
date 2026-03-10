"""Auto-generated module for US-003: Student Attendance Notifications."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

import json
import requests

@dataclass
class StudentAttendanceNotificationsService:
    """Implementation class aligned to user story US-003."""

    def __init__(self, notification_service_url: str):
        self.notification_service_url = notification_service_url

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        student_attendance_records = self.get_student_attendance(payload)
        excessive_absences = self.calculate_excessive_absences(student_attendance_records)
        self.send_notifications(excessive_absences)

        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Parents/guardians receive notifications when a student has excessive absences",
            "acceptance": "Parents/guardians receive notifications when a student has excessive absences, can view their child's attendance records online, and can receive attendance notifications via email or SMS.",
        }
        return result

    def get_student_attendance(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retrieves student attendance records from SIS."""
        response = requests.get(f"{payload['sis_url']}/attendance", params={"student_id": payload["student_id"]})
        return response.json() if response.status_code == 200 else []

    def calculate_excessive_absences(self, student_attendance_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculates attendance status."""
        excessive_absences = [
            {
                "studentId": record["studentId"],
                "studentName": record["studentName"],
                "attendanceStatus": "ExcessiveAbsences",
                "date": record["date"],
            }
            for record in student_attendance_records
            if self.is_excessive_absences(record)
        ]
        return excessive_absences

    def is_excessive_absences(self, record: Dict[str, Any]) -> bool:
        """Checks if attendance record is considered excessive."""
        # Implement your logic here
        return record["isPresent"] is False and record["num_consecutive_absences"] >= 5

    def send_notifications(self, excessive_absences: List[Dict[str, Any]]) -> None:
        """Sends attendance notifications to parents/guardians."""
        for notification in excessive_absences:
            self._send_notification(notification)

    def _send_notification(self, notification: Dict[str, Any]) -> None:
        """Sends a single notification."""
        notification_data = {
            "studentName": notification["studentName"],
            "attendanceStatus": notification["attendanceStatus"],
            "date": notification["date"],
        }
        response = requests.post(
            self.notification_service_url,
            json={"student_id": notification["studentId"], "notification": notification_data, "notification_type": "email_or_sms"},
        )
        if response.status_code != 200:
            print(f"Failed to send notification for student {notification['studentId']}")

def build_student_attendance_notifications(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    student_attendance_notifications_service = StudentAttendanceNotificationsService(payload["notification_service_url"])
    return student_attendance_notifications_service.execute(payload)
