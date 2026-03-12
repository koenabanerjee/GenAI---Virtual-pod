from pathlib import Path

from virtual_dev_pod.repository import TemplateRepository


def test_template_rendering():
    root = Path(__file__).resolve().parents[1]
    repo = TemplateRepository(root / "org_repository/templates")
    rendered = repo.render(
        "user_story_template.md",
        story_id="US-001",
        title="Sample",
        persona="PM",
        goal="Track progress",
        benefit="Visibility",
        priority="High",
        acceptance_criteria="- AC1",
    )
    assert "US-001" in rendered
    assert "Track progress" in rendered
