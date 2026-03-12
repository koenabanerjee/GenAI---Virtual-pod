from __future__ import annotations

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import UserStory
from virtual_dev_pod.utils import extract_json_payload, trim_words


class BusinessAnalystAgent(BaseAgent):
    def analyze_requirements(
        self, requirements: str, *, max_user_stories: int = 5
    ) -> list[UserStory]:
        template = self.template_repository.get_template("user_story_template.md")
        prompt = f"""
You are a Business Analyst Agent in an enterprise virtual development pod.
Use the enterprise standards below and convert the business requirements into user stories.

Enterprise standards:
{self.knowledge_context}

Output strictly valid JSON with this shape:
[
  {{
    "story_id": "US-001",
    "title": "short title",
    "persona": "role",
    "goal": "what user needs",
    "benefit": "business value",
    "priority": "High|Medium|Low",
    "acceptance_criteria": ["criterion 1", "criterion 2"]
  }}
]

Limit to {max_user_stories} stories.
Template reference:
{template}

Business requirements:
{requirements}
"""
        llm_output = self._call_llm(prompt)
        parsed = extract_json_payload(llm_output)
        stories = self._parse_story_payload(parsed, max_user_stories=max_user_stories)
        if stories:
            return stories
        return self._fallback_stories(requirements, max_user_stories=max_user_stories)

    def render_user_stories(self, stories: list[UserStory]) -> str:
        blocks: list[str] = []
        for story in stories:
            criteria = "\n".join(f"- {item}" for item in story.acceptance_criteria)
            block = self.template_repository.render(
                "user_story_template.md",
                story_id=story.story_id,
                title=story.title,
                persona=story.persona,
                goal=story.goal,
                benefit=story.benefit,
                priority=story.priority,
                acceptance_criteria=criteria,
            )
            blocks.append(block.strip())
        return "\n\n".join(blocks).strip() + "\n"

    def _parse_story_payload(
        self, payload: dict | list | None, *, max_user_stories: int
    ) -> list[UserStory]:
        if not isinstance(payload, list):
            return []
        stories: list[UserStory] = []
        for idx, item in enumerate(payload[:max_user_stories], start=1):
            if not isinstance(item, dict):
                continue
            criteria = item.get("acceptance_criteria", [])
            if not isinstance(criteria, list):
                criteria = [str(criteria)]
            clean_criteria = [str(entry).strip() for entry in criteria if str(entry).strip()]
            stories.append(
                UserStory(
                    story_id=str(item.get("story_id", f"US-{idx:03}")),
                    title=str(item.get("title", f"User Story {idx}")),
                    persona=str(item.get("persona", "Project Lead")),
                    goal=str(item.get("goal", "Deliver requested capability")),
                    benefit=str(item.get("benefit", "Provide business value")),
                    priority=str(item.get("priority", "Medium")),
                    acceptance_criteria=clean_criteria
                    or ["Expected behavior is verified and documented."],
                )
            )
        return stories

    def _fallback_stories(
        self, requirements: str, *, max_user_stories: int
    ) -> list[UserStory]:
        normalized = [
            line.strip("- ").strip()
            for line in requirements.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if not normalized:
            normalized = ["Implement the requested software capability."]

        stories: list[UserStory] = []
        for idx, line in enumerate(normalized[:max_user_stories], start=1):
            title = trim_words(line, max_words=12)
            stories.append(
                UserStory(
                    story_id=f"US-{idx:03}",
                    title=title,
                    persona="Project Lead",
                    goal=line,
                    benefit="The project delivers traceable SDLC outcomes.",
                    priority="High" if idx == 1 else "Medium",
                    acceptance_criteria=[
                        "A standardized artifact is produced for this requirement.",
                        "Generated outputs can be traced to the source requirement.",
                        "The output is reviewable by the project manager.",
                    ],
                )
            )
        return stories
