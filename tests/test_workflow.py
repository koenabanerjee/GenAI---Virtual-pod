import shutil
import threading
import time
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
    assert result.stage_status.get("management") == "completed"
    assert not (result.run_dir / "reports" / "product_manager_summary.md").exists()
    status_answer = pod.pm_chat("Give me current progress and stage status")
    quality_answer = pod.pm_chat("How is test quality and failures?")
    artifact_answer = pod.pm_chat("Show me code artifacts and files")
    assert "Progress view" in status_answer
    assert "Stage status:" in status_answer
    assert ("Quality view" in quality_answer) or ("Testing update" in quality_answer)
    assert ("Artifact view" in artifact_answer) or ("Developer update" in artifact_answer)
    assert len({status_answer, quality_answer, artifact_answer}) == 3
    assert result.metadata_path is not None
    assert result.metadata_path.exists()


def test_pm_chat_supports_live_progress_queries():
    root = Path(__file__).resolve().parents[1]
    tmp_root = root / "artifacts" / "_test_tmp_workflow_live"
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

    run_holder: dict[str, object] = {}

    def _worker() -> None:
        run_holder["result"] = pod.run_sdlc(
            "Create a virtual dev pod that writes code and tests from requirements.",
            project_name="test-live-chat",
        )

    worker = threading.Thread(target=_worker, daemon=True)
    worker.start()

    saw_live_reply = False
    for _ in range(120):
        response = pod.pm_chat("What is the current progress?")
        if response.startswith("Live run `"):
            saw_live_reply = True
            break
        time.sleep(0.05)

    worker.join(timeout=120)
    assert saw_live_reply
    assert "result" in run_holder
