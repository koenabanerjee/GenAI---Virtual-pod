"""Auto-generated module for US-002: Create a user interface for teachers to view student performance reports."""

from __future__ import annotations
from typing import Dict, Any

import requests

@dataclass
class CreateAUserInterfaceForTeachersToViewStudentPerformanceReportsService:
    """Implementation class aligned to user story US-002."""

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute user story logic."""
        auth_response = self._authenticate(payload)
        student_id = auth_response["data"]["user_id"]
        student_report = self._get_student_report(student_id)

        result = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Generated student performance report for teacher",
            "acceptance": {
                "student_report": student_report,
            },
        }
        return result

    def _authenticate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate teacher and get user data."""
        auth_url = "http://localhost:3001/api/auth/login"
        auth_data = {
            "username": payload["teacher"]["username"],
            "password": payload["teacher"]["password"],
        }
        response = requests.post(auth_url, json=auth_data)
        response.raise_for_status()
        return response.json()

    def _get_student_report(self, student_id: str) -> Dict[str, Any]:
        """Get student performance report."""
        report_url = f"http://localhost:5001/api/students/{student_id}/report"
        response = requests.get(report_url)
        response.raise_for_status()
        return response.json()


def build_create_a_user_interface_for_teachers_to_view_student_performance(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    service = CreateAUserInterfaceForTeachersToViewStudentPerformanceReportsService()
    return service.execute(payload)
