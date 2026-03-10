"""Auto-generated module for US-001: Student Attendance Marking."""

from datetime import date
from typing import Dict, List

@dataclass
class StudentAttendanceMarkingService:
    """Implementation class aligned to user story US-001."""

    def __init__(self, class_id: str, sis_client):
        self.class_id = class_id
        self.sis_client = sis_client

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        input = payload.get("input", {})
        date = input.get("date")
        student_ids = input.get("studentIds")

        if not all([isinstance(id, str) for id in student_ids]):
            return {
                "story_id": self.story_id,
                "status": "failed",
                "input": input,
                "summary": "Invalid student IDs",
                "acceptance": "As a teacher, I can mark attendance for all students in a class",
            }

        attendance_marks = self._mark_attendance(date, student_ids)

        return {
            "story_id": self.story_id,
            "status": "success",
            "input": input,
            "summary": "Attendance marks saved for class {} on {}".format(self.class_id, date),
            "acceptance": "Attendance marks are saved and persist in the system",
            "output": {"attendanceMarks": attendance_marks},
        }

    def _mark_attendance(self, date: date, student_ids: List[str]) -> List[Dict[str, Any]]:
        attendance_marks = []
        for student_id in student_ids:
            student_attendance = self.sis_client.get_student_attendance(self.class_id, student_id, date)
            attendance_marks.append(self._update_attendance_mark(student_attendance))

        self.sis_client.save_attendance_marks(self.class_id, date, attendance_marks)

        return attendance_marks

    def _update_attendance_mark(self, student_attendance: Dict[str, Any]) -> Dict[str, Any]:
        student_attendance["isPresent"] = True
        return student_attendance

def build_student_attendance_marking(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    service = StudentAttendanceMarkingService("class_id_goes_here", mock_sis_client)
    return service.execute(payload)
