"""Auto-generated module for US-003: As a user, I want to be able to delete tasks from the todo app"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AsAUserIWantToBeAbleToDeleteTasksFromTheTodoAppService:
    """Implementation class aligned to user story US-003."""

    def __init__(self, task_service, database):
        self.task_service = task_service
        self.database = database

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload["task_id"]
        confirmation = payload.get("confirmation", True)

        if not confirmation:
            return {
                "story_id": self.story_id,
                "status": "failed",
                "input": payload,
                "summary": "Task deletion was not confirmed by the user.",
                "acceptance": "User cannot delete a task without confirmation.",
            }

        task = self.task_service.get_task(task_id)
        if not task:
            return {
                "story_id": self.story_id,
                "status": "failed",
                "input": payload,
                "summary": "Task not found.",
                "acceptance": "User cannot delete a non-existent task.",
            }

        self.database.begin_transaction()
        self.task_service.delete_task(task_id)
        self.database.commit()

        return {
            "story_id": self.story_id,
            "status": "success",
            "input": payload,
            "summary": f"Task '{task['title']}' was deleted.",
            "acceptance": "User can delete a task from the todo list.",
        }


def build_as_a_user_i_want_to_be_able_to_delete_tasks_from_the_todo_app(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    todo_list_component, task_service, database = payload["components"]
    return AsAUserIWantToBeAbleToDeleteTasksFromTheTodoAppService(task_service, database).execute(payload)

# Assuming the following components are imported from other modules
# import TodoListComponent
# import TaskService
# import Database

# And the following methods are implemented in the respective components
# def get_task(self, task_id: str) -> Dict[str, Any]:
#     ...
#
# def delete_task(self, task_id: str):
#     ...
#
# def begin_transaction(self):
#     ...
#
# def commit(self):
#     ...
