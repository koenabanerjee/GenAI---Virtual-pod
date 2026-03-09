"""Auto-generated module for US-003: Manage Member Information."""

from __future__ import annotations
from datetime import datetime
from typing import Any, Dict

@dataclass
class ManageMemberInformationService:
    """Implementation class aligned to user story US-003."""

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def add_member(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        member = self._validate_member_data(payload)
        new_member = self.member_repository.add_member(member)
        return {
            "story_id": self.story_id,
            "status": "success",
            "input": payload,
            "summary": "New member added",
            "acceptance": {
                "member_id": new_member["id"],
                "first_name": new_member["firstName"],
                "last_name": new_member["lastName"],
                "email": new_member["email"],
                "phone_number": new_member["phoneNumber"],
                "address": new_member["address"],
                "membership_type": new_member["membershipType"],
                "membership_expiration_date": new_member["membershipExpirationDate"].strftime("%Y-%m-%d"),
                "is_active": new_member["isActive"]
            }
        }

    def edit_member(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        member_id = int(payload["memberId"])
        updated_member = self._validate_member_data(payload)
        member = self.member_repository.get_member_by_id(member_id)

        if not member:
            return {
                "story_id": self.story_id,
                "status": "error",
                "input": payload,
                "summary": "Member not found",
                "acceptance": {}
            }

        updated_member["id"] = member_id
        self.member_repository.update_member(member_id, updated_member)

        return {
            "story_id": self.story_id,
            "status": "success",
            "input": payload,
            "summary": "Member record updated",
            "acceptance": {
                "member_id": member_id,
                "first_name": updated_member["firstName"],
                "last_name": updated_member["lastName"],
                "email": updated_member["email"],
                "phone_number": updated_member["phoneNumber"],
                "address": updated_member["address"],
                "membership_type": updated_member["membershipType"],
                "membership_expiration_date": updated_member["membershipExpirationDate"].strftime("%Y-%m-%d"),
                "is_active": updated_member["isActive"]
            }
        }

    def delete_member(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        member_id = int(payload["memberId"])
        member = self.member_repository.get_member_by_id(member_id)

        if not member:
            return {
                "story_id": self.story_id,
                "status": "error",
                "input": payload,
                "summary": "Member not found",
                "acceptance": {}
            }

        if member["isActive"]:
            return {
                "story_id": self.story_id,
                "status": "error",
                "input": payload,
                "summary": "Member is active, cannot be deleted",
                "acceptance": {}
            }

        self.member_repository.delete_member(member_id)
        return {
            "story_id": self.story_id,
            "status": "success",
            "input": payload,
            "summary": "Member record deleted",
            "acceptance": {}
        }

    def _validate_member_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        member = {
            "firstName": payload["firstName"],
            "lastName": payload["lastName"],
            "email": payload["email"],
            "phoneNumber": payload["phoneNumber"],
            "address": payload["address"],
            "membershipType": payload["membershipType"],
            "membershipExpirationDate": datetime.strptime(payload["membershipExpirationDate"], "%Y-%m-%d"),
            "isActive": bool(payload["isActive"])
        }

        if not all([member[key] for key in member]):
            raise ValueError("Missing required fields")

        return member


def build_manage_member_information(payload: Dict[str, Any]) -> Dict
