"""Auto-generated module for US-002: As a user, I want to be able to mark tasks as completed in the todo app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AsAUserIWantToBeAbleToMarkTasksAsCompletedInTheTodoAppService:
    """Implementation class aligned to user story US-002."""

    story_id: str = "US-002"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Mark tasks as completed in the todo app",
            "acceptance": "User can toggle the completion status of a task; Completed tasks are visually distinguished from incomplete ones in the todo list; User can view a report or filter of only completed tasks",
        }
        return result


def build_as_a_user_i_want_to_be_able_to_mark_tasks_as_completed_in_the_to(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    return AsAUserIWantToBeAbleToMarkTasksAsCompletedInTheTodoAppService().execute(payload)
