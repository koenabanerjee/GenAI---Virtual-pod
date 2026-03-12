import shutil
import json
from pathlib import Path

import pytest

from virtual_dev_pod.config import PodConfig
from virtual_dev_pod.models import UserStory
from virtual_dev_pod.agents.ui_designer import UIDesignerAgent
from virtual_dev_pod.workflow import VirtualDevelopmentPod
from virtual_dev_pod.llm_factory import build_llm
from virtual_dev_pod.repository import TemplateRepository


def test_ui_designer_generates_mockups(tmp_path):
    """Test that UI Designer Agent generates HTML mockups and specs."""
    root = Path(__file__).resolve().parents[1]
    
    # Create mock LLM and template repo
    llm = build_llm(
        "mock",
        model_id="mock",
        api_token=None,
        temperature=0.2,
        max_tokens=800,
        require_real_llm=False,
    )
    template_repo = TemplateRepository(root / "org_repository/templates")
    
    ui_designer = UIDesignerAgent(
        name="UI Designer Agent",
        llm=llm,
        template_repository=template_repo,
        knowledge_dir=root / "org_repository/knowledge",
    )
    
    # Create sample user stories
    stories = [
        UserStory(
            story_id="US-001",
            title="User Login",
            persona="End User",
            goal="login to the application",
            benefit="Secure access to user data",
            priority="High",
            acceptance_criteria=["Email/password input", "Submit button", "Error handling"],
        ),
        UserStory(
            story_id="US-002",
            title="View Dashboard",
            persona="End User",
            goal="see all important information",
            benefit="Quick overview of key metrics",
            priority="High",
            acceptance_criteria=["Display charts", "Show statistics", "Responsive layout"],
        ),
    ]
    
    # Generate UI artifacts
    ui_artifacts = ui_designer.generate_ui_artifacts(stories, output_dir=tmp_path)
    
    # Verify artifacts were created
    assert len(ui_artifacts) > 0
    
    # Verify spec files exist
    assert (tmp_path / "ui_spec.md").exists()
    assert (tmp_path / "pages.json").exists()
    
    # Verify HTML mockups were created
    mockups_dir = tmp_path / "mockups"
    assert mockups_dir.exists()
    
    # Check that HTML files contain expected content
    html_files = list(mockups_dir.glob("*.html"))
    for html_file in html_files:
        content = html_file.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "<style>" in content
        assert "navbar" in content.lower()


def test_ui_designer_fallback_mode(tmp_path):
    """Test that UI Designer generates fallback specs when LLM is unavailable,
    and that JSON normalization handles legacy single-page formats.
    """
    root = Path(__file__).resolve().parents[1]
    
    llm = build_llm(
        "mock",
        model_id="mock",
        api_token=None,
        temperature=0.2,
        max_tokens=800,
        require_real_llm=False,
    )
    template_repo = TemplateRepository(root / "org_repository/templates")
    
    ui_designer = UIDesignerAgent(
        name="UI Designer Agent",
        llm=llm,
        template_repository=template_repo,
        knowledge_dir=root / "org_repository/knowledge",
    )
    
    stories = [
        UserStory(
            story_id="US-001",
            title="Test Feature",
            persona="Tester",
            goal="test the system",
            benefit="Quality assurance",
            priority="Medium",
            acceptance_criteria=["Works as expected"],
        ),
    ]
    
    # Run the full artifact generation to exercise normalization path
    ui_artifacts = ui_designer.generate_ui_artifacts(stories, output_dir=tmp_path)
    assert len(ui_artifacts) >= 1

    pages_path = tmp_path / "pages.json"
    assert pages_path.exists()
    data = json.loads(pages_path.read_text(encoding="utf-8"))
    # after normalization we must have a list under `pages`
    assert "pages" in data and isinstance(data["pages"], list)
    assert data["pages"][0]["name"]

    # simulate legacy output by patching _generate_ui_spec to return unnormalized data
    legacy = {
        "name": "Legacy Page",
        "story_id": "US-001",
        "components": ["A", "B"],
        "layout": "vertical",
        "description": "old format",
    }

    def fake_generate(stories_list):
        # ui_spec can be simple markdown; we only care about pages_data
        return "# legacy spec", legacy

    ui_designer._generate_ui_spec = fake_generate
    ui_artifacts3 = ui_designer.generate_ui_artifacts(stories, output_dir=tmp_path)
    # normalization should occur, yielding at least one artifact
    assert len(ui_artifacts3) == 1
    pages_contents = json.loads(pages_path.read_text(encoding="utf-8"))
    assert "pages" in pages_contents
    assert isinstance(pages_contents["pages"], list)
    assert pages_contents["pages"][0]["name"] == "Legacy Page"


def test_workflow_includes_ui_stage():
    """Test that the SDLC workflow includes UI Designer Agent step."""
    root = Path(__file__).resolve().parents[1]
    tmp_root = root / "artifacts" / "_test_tmp_workflow_ui"
    if tmp_root.exists():
        shutil.rmtree(tmp_root, ignore_errors=True)
    tmp_root.mkdir(parents=True, exist_ok=True)

    config = PodConfig(
        base_dir=root,
        template_dir=root / "org_repository/templates",
        knowledge_dir=root / "org_repository/knowledge",
        artifact_root=tmp_root / "artifacts",
        vector_db_dir=tmp_root / "vector_db",
        llm_provider="mock",
        hf_model_id="mistralai/Mistral-7B-Instruct-v0.2",
        hf_api_token=None,
        require_real_llm=False,
        llm_temperature=0.2,
        llm_max_tokens=800,
        enable_crewai=False,
        max_user_stories=2,
        top_k_context=3,
        fast_mode=False,
        execute_tests=False,
        use_chromadb=False,
    )
    
    pod = VirtualDevelopmentPod(config=config)
    result = pod.run_sdlc(
        "Create a simple task management app with login and dashboard.",
        project_name="ui-test-project",
    )
    
    # Verify UI artifacts were generated
    assert len(result.ui_artifacts) > 0
    
    # Verify UI stage completed
    assert result.stage_status.get("ui_design") == "completed"
    
    # Verify UI files exist
    ui_dir = result.run_dir / "ui"
    assert (ui_dir / "ui_spec.md").exists()
    assert (ui_dir / "pages.json").exists()
    assert (ui_dir / "mockups").exists()
    
    # Verify HTML mockups exist
    html_files = list((ui_dir / "mockups").glob("*.html"))
    assert len(html_files) > 0
