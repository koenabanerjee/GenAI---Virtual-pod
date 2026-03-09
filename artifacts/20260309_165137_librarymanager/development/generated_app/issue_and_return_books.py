"""Auto-generated module for US-002: Issue and Return Books."""

from __future__ import annotations
from datetime import datetime
from typing import Dict, List

import pydantic

from library_management_system import Book, LibraryManagementSystem
from member_database import Member, MemberDatabase
from checkout_event import CheckoutEvent
from checkin_event import CheckinEvent

@dataclass
class IssueAndReturnBooksService:
    library_management_system: LibraryManagementSystem
    member_database: MemberDatabase

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        action = payload["action"]
        book_id = int(payload["book_id"])
        member_id = int(payload["member_id"])

        result = {
            "story_id": "US-002",
            "status": "implemented",
            "input": payload,
            "summary": "Library staff can check out and check in books for members",
            "acceptance": {
                "As a library staff member, I can check out a book to a member": "",
                "As a library staff member, I can check in a book when it is returned": "",
                "As a library member, I receive a receipt or confirmation when a book is checked out or returned": "",
            },
        }

        if action == "checkout":
            member = self.member_database.get_member(member_id)
            book = self.library_management_system.get_book(book_id)

            if book is None or member is None or book.is_checked_out:
                result["error"] = "Invalid input"
                return result

            self.library_management_system.checkout_book(book_id, member_id)
            self.member_database.update_member(member)
            result["output"] = CheckoutEvent(book, member, datetime.now())

        elif action == "checkin":
            member = self.member_database.get_member(member_id)
            book = self.library_management_system.get_book(book_id)

            if book is None or member is None or not book.is_checked_out:
                result["error"] = "Invalid input"
                return result

            self.library_management_system.checkin_book(book_id)
            self.member_database.update_member(member)
            result["output"] = CheckinEvent(book, member, datetime.now())

        return result


def build_issue_and_return_books(payload: Dict[str, Any]) -> Dict[str, Any]:
    issue_and_return_books = IssueAndReturnBooksService(
        LibraryManagementSystem(), MemberDatabase()
    )
    return issue_and_return_books.execute(payload)
