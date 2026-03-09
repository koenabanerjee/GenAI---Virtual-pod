from __future__ import annotations

import re
from pathlib import Path

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import CodeArtifact, UserStory
from virtual_dev_pod.utils import safe_class_name, slugify


class DeveloperAgent(BaseAgent):
    def build_modules(
        self,
        stories: list[UserStory],
        *,
        output_dir: Path,
        design_context_by_story: dict[str, str] | None = None,
    ) -> list[CodeArtifact]:
        output_dir.mkdir(parents=True, exist_ok=True)
        init_file = output_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# Generated package for Virtual Development Pod\n")

        artifacts: list[CodeArtifact] = []
        for story in stories:
            module_name = slugify(story.title)[:64].strip("_") or "generated_module"
            class_name = safe_class_name(story.title)
            module_file = output_dir / f"{module_name}.py"

            generated = self._generate_module_content(
                story=story,
                module_name=module_name,
                class_name=class_name,
                design_context=(design_context_by_story or {}).get(story.story_id, ""),
            )
            module_file.write_text(generated, encoding="utf-8")

            artifacts.append(
                CodeArtifact(
                    story_id=story.story_id,
                    module_name=module_name,
                    file_path=module_file,
                    summary=story.goal,
                )
            )
        return artifacts

    def _generate_module_content(
        self,
        *,
        story: UserStory,
        module_name: str,
        class_name: str,
        design_context: str = "",
    ) -> str:
        template = self.template_repository.get_template("code_module_template.py.tmpl")
        prompt = f"""
You are a Senior Python Developer Agent.
Generate production-grade Python code for this user story.
Do not use placeholders, dummy values, or mock text in the implementation logic.
Return Python code only.

Story ID: {story.story_id}
Title: {story.title}
Persona: {story.persona}
Goal: {story.goal}
Business benefit: {story.benefit}
Acceptance criteria:
{chr(10).join(f"- {entry}" for entry in story.acceptance_criteria)}

Design guidance:
{design_context or "No dedicated design spec available; infer best-practice structure."}

Required contract:
- Define class `{class_name}`.
- Define function `build_{module_name}(payload: Dict[str, Any]) -> Dict[str, Any]`.
- Returned dict must include keys: story_id, status, input, summary, acceptance.

Use this enterprise template as structural guidance:
{template}
"""
        llm_output = self._call_llm(prompt)
        code = self._extract_python(llm_output)
        if self._module_meets_contract(code, module_name=module_name, class_name=class_name):
            return code

        criteria_summary = "; ".join(story.acceptance_criteria)
        return self.template_repository.render(
            "code_module_template.py.tmpl",
            module_name=module_name,
            class_name=class_name,
            story_id=story.story_id,
            story_title=story.title.replace('"', "'"),
            goal=story.goal.replace('"', "'"),
            criteria_summary=criteria_summary.replace('"', "'"),
        )

    def _extract_python(self, text: str) -> str:
        if not text:
            return ""
        matches = re.findall(r"```python\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0].strip() + "\n"
        generic = re.findall(r"```\s*(.*?)```", text, flags=re.DOTALL)
        if generic:
            return generic[0].strip() + "\n"
        return text.strip() + "\n"

    def _looks_like_python(self, text: str) -> bool:
        text = text.strip()
        return bool(text) and ("def " in text or "class " in text)

    def _module_meets_contract(
        self, text: str, *, module_name: str, class_name: str
    ) -> bool:
        if not self._looks_like_python(text):
            return False
        required_snippets = [
            f"class {class_name}",
            f"def build_{module_name}",
            '"story_id"',
            '"status"',
        ]
        return all(snippet in text for snippet in required_snippets)
