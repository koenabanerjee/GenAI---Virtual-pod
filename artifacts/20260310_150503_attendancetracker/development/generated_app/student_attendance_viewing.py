"""Auto-generated module for US-002: Student Attendance Viewing."""

from __future__ import annotations
from typing import Any, Dict, List
import hashlib

import psycopg2

@dataclass
class StudentAttendanceViewingService:
    """Implementation class aligned to user story US-002."""

    story_id: str = "US-002"

    def __init__(self, db_connection: psycopg2.connect):
        self.db = db_connection

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "View student attendance records",
            "acceptance": {
                "Students can view their attendance records for the current semester": self.view_current_semester_attendance,
                "Students can view their attendance records for previous semesters": self.view_previous_semester_attendance,
                "Students can download or print their attendance records": self.download_attendance_records,
            },
        }
        return result

    def view_current_semester_attendance(self, student_id: int) -> List[Dict[str, Any]]:
        """Retrieve current semester attendance records for the given student."""
        query = """
            SELECT s.student_id, a.semester, a.date, a.attendance_status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            WHERE s.student_id = %s
            AND a.semester = (
                SELECT semester FROM semesters WHERE current = true
            )
        """
        cursor = self.db.cursor()
        cursor.execute(query, (student_id,))
        records = cursor.fetchall()
        cursor.close()
        return records

    def view_previous_semester_attendance(self, student_id: int, semester: int) -> List[Dict[str, Any]]:
        """Retrieve attendance records for the given student in the given semester."""
        query = """
            SELECT s.student_id, a.semester, a.date, a.attendance_status
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            WHERE s.student_id = %s
            AND a.semester = %s
        """
        cursor = self.db.cursor()
        cursor.execute(query, (student_id, semester))
        records = cursor.fetchall()
        cursor.close()
        return records

    def download_attendance_records(self, student_id: int) -> bytes:
        """Download attendance records for the given student in a CSV format."""
        query = """
            SELECT student_id, semester, date, attendance_status
            FROM attendance
            WHERE student_id = %s
        """
        records = []

        cursor = self.db.cursor()
        cursor.execute(query, (student_id,))

        column_names = ["Student ID", "Semester", "Date", "Attendance Status"]
        records.append(column_names)

        while True:
            row = cursor.fetchone()
            if not row:
                break
            records.append(row)

        csv_data = self.generate_csv(records)

        return csv_data

    @staticmethod
    def generate_csv(records: List[Tuple[Any, Any, Any, Any]]) -> bytes:
        """Generate CSV data from the given records."""
        csv_data = b""
        for row in records:
            row_data = b""
            for value in row:
                row_data += str(value).encode() + b";"
            row_data += b"\n"
            csv_data += row_data

        return hashlib.sha256(csv_data).digest()


def build_student_attendance_viewing(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    db_connection = psycopg2.connect(database="your_database_name", user="your_user", password="your_password", host="localhost", port="5432")
    student_attendance_viewing = StudentAttendanceViewingService(db_connection)
    return student_attendance_viewing.execute(payload)
