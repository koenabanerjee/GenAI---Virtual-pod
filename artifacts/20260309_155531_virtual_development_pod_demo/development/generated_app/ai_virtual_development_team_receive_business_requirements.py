"""Auto-generated module for US-001: AI Virtual Development Team - Receive Business Requirements."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AiVirtualDevelopmentTeamReceiveBusinessRequirementsService:
    """Implementation class aligned to user story US-001."""

    story_id: str = "US-001"

    def extract_key_information(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key information from business requirements."""
        story_title = payload["title"]
        goal = "Provide clear and concise business requirements to the AI Virtual Development Team"
        acceptance_criteria = [
            {"key": "AI system can accurately interpret and understand business requirements"},
            {"key": "System can identify key information and extract relevant details from requirements"},
        ]
        return {
            "story_title": story_title,
            "goal": goal,
            "acceptance_criteria": acceptance_criteria,
        }

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        extracted_info = self.extract_key_information(payload)
        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "received",
            "input": payload,
            "summary": extracted_info["goal"],
            "acceptance": extracted_info,
        }
        return result


def build_ai_virtual_development_team_receive_business_requirements(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    ai_team = AiVirtualDevelopmentTeamReceiveBusinessRequirementsService()
    return ai_team.execute(payload)
