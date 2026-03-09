"""Integration tests for generated modules."""

from generated_app.maintain_book_records import build_maintain_book_records
from generated_app.issue_and_return_books import build_issue_and_return_books
from generated_app.manage_member_information import build_manage_member_information


def test_generated_app_integration():
    result_1 = build_maintain_book_records({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_issue_and_return_books({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_manage_member_information({'input': 'sample'})
    assert isinstance(result_3, dict)
