import shutil
from pathlib import Path

from virtual_dev_pod.config import PodConfig
from virtual_dev_pod.workflow import VirtualDevelopmentPod


def test_workflow_generates_artifacts():
    root = Path(__file__).resolve().parents[1]
    tmp_root = root / "artifacts" / "_test_tmp_workflow"
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
        max_user_stories=3,
        top_k_context=3,
        fast_mode=False,
        execute_tests=True,
        use_chromadb=False,
    )
    pod = VirtualDevelopmentPod(config=config)
    result = pod.run_sdlc(
        "Create a virtual dev pod that writes code and tests from requirements.",
        project_name="test-project",
    )

    assert result.user_stories
    assert result.design_artifacts
    assert result.code_artifacts
    assert result.test_artifacts
    assert result.test_execution is not None
    assert result.pm_summary
    assert result.stage_status.get("management") == "completed"
    assert (result.run_dir / "reports" / "product_manager_summary.md").exists()
    assert "status overview" in pod.pm_chat("Give me stage status and missing steps")
    assert result.metadata_path is not None
    assert result.metadata_path.exists()
