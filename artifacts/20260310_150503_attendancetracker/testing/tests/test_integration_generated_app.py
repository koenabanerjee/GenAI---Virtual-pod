"""Integration tests for generated modules."""

from generated_app.student_attendance_marking import build_student_attendance_marking
from generated_app.student_attendance_viewing import build_student_attendance_viewing
from generated_app.student_attendance_notifications import build_student_attendance_notifications


def test_generated_app_integration():
    result_1 = build_student_attendance_marking({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_student_attendance_viewing({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_student_attendance_notifications({'input': 'sample'})
    assert isinstance(result_3, dict)
