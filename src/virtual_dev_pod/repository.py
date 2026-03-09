from __future__ import annotations

from pathlib import Path


class TemplateRepository:
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir

    def get_template(self, template_name: str) -> str:
        path = self.template_dir / template_name
        if not path.exists():
            raise FileNotFoundError(f"Template not found: {path}")
        return path.read_text(encoding="utf-8")

    def render(self, template_name: str, **kwargs: str) -> str:
        template = self.get_template(template_name)
        return template.format(**kwargs)
