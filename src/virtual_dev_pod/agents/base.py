from __future__ import annotations

from pathlib import Path

from virtual_dev_pod.llm_factory import LLMGateway
from virtual_dev_pod.repository import TemplateRepository


class BaseAgent:
    def __init__(
        self,
        *,
        name: str,
        llm: LLMGateway,
        template_repository: TemplateRepository,
        knowledge_dir: Path,
    ):
        self.name = name
        self.llm = llm
        self.template_repository = template_repository
        self.knowledge_dir = knowledge_dir
        self.knowledge_context = self._load_knowledge()

    def _load_knowledge(self) -> str:
        documents: list[str] = []
        if not self.knowledge_dir.exists():
            return ""
        for file_path in sorted(self.knowledge_dir.glob("*.md")):
            documents.append(file_path.read_text(encoding="utf-8"))
        return "\n\n".join(documents)

    def _call_llm(self, prompt: str) -> str:
        return self.llm.generate(prompt, max_tokens=1200)

    def _is_mock_llm(self) -> bool:
        return bool(getattr(self.llm, "is_mock", False))
