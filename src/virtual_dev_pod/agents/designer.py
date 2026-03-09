from __future__ import annotations

from pathlib import Path

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import DesignArtifact, UserStory
from virtual_dev_pod.utils import slugify


class DesignAgent(BaseAgent):
    def create_design_artifacts(
        self, stories: list[UserStory], *, output_dir: Path
    ) -> list[DesignArtifact]:
        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts: list[DesignArtifact] = []
        for story in stories:
            component_name = slugify(story.title)[:64].strip("_") or "component"
            file_path = output_dir / f"{component_name}_design.md"
            content = self._generate_design_content(
                story=story, component_name=component_name
            )
            file_path.write_text(content, encoding="utf-8")
            artifacts.append(
                DesignArtifact(
                    story_id=story.story_id,
                    component_name=component_name,
                    file_path=file_path,
                    summary=story.goal,
                )
            )
        return artifacts

    def _generate_design_content(self, *, story: UserStory, component_name: str) -> str:
        template = self.template_repository.get_template("design_spec_template.md")
        prompt = f"""
You are a Solution Design Agent.
Create a concise software design spec in markdown for this story.

Story ID: {story.story_id}
Title: {story.title}
Goal: {story.goal}
Business Benefit: {story.benefit}
Acceptance Criteria:
{chr(10).join(f"- {item}" for item in story.acceptance_criteria)}

Return markdown only with sections:
1) Component Scope
2) Architecture and Interfaces
3) Data Contracts
4) Risks and Mitigations
5) Non-functional considerations
"""
        llm_output = self._call_llm(prompt).strip()
        if llm_output and llm_output != "MOCK_PROVIDER_ACTIVE":
            return llm_output
        return self.template_repository.render(
            "design_spec_template.md",
            story_id=story.story_id,
            title=story.title,
            component_name=component_name,
            goal=story.goal,
            benefit=story.benefit,
            acceptance_criteria="\n".join(
                f"- {item}" for item in story.acceptance_criteria
            ),
        )
