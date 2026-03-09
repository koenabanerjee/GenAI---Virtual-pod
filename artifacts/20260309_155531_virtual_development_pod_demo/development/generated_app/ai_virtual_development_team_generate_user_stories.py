"""Auto-generated module for US-002: AI Virtual Development Team - Generate User Stories."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AiVirtualDevelopmentTeamGenerateUserStoriesService:
    """Implementation class aligned to user story US-002."""

    story_id: str = "US-002"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        business_requirement = payload["business_requirement"]
        persona = business_requirement["persona"]
        goal = business_requirement["goal"]
        benefits = business_requirement["benefits"]
        acceptance_criteria = business_requirement["acceptance_criteria"]

        title = f"As a {persona}, I want {goal} so that {', '.join(benefits)}"
        summary = f"Generate user stories based on business requirements: {goal}"
        criteria_summary = ", ".join([f"{criterion['description']}" for criterion in acceptance_criteria])

        return {
            "story_id": self.story_id,
            "status": "to_do",
            "input": payload,
            "summary": summary,
            "acceptance": {
                "title": title,
                "criteria": acceptance_criteria,
            },
        }

def build_ai_virtual_development_team_generate_user_stories(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    return AiVirtualDevelopmentTeamGenerateUserStoriesService().execute(payload)
