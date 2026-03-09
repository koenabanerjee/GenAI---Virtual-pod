from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from virtual_dev_pod.agents import (
    BusinessAnalystAgent,
    DesignAgent,
    DeveloperAgent,
    ProductManagerAgent,
    TestingAgent,
)
from virtual_dev_pod.config import PodConfig
from virtual_dev_pod.crew_adapter import CrewAIPlanner
from virtual_dev_pod.llm_factory import build_llm, llm_diagnostics
from virtual_dev_pod.models import RunResult
from virtual_dev_pod.repository import TemplateRepository
from virtual_dev_pod.utils import slugify, utc_timestamp
from virtual_dev_pod.vector_store import ArtifactVectorStore


class VirtualDevelopmentPod:
    def __init__(self, config: PodConfig | None = None):
        root = Path(__file__).resolve().parents[2]
        self.config = config or PodConfig.from_env(base_dir=root)
        self.template_repository = TemplateRepository(self.config.template_dir)
        self.llm = build_llm(
            self.config.llm_provider,
            model_id=self.config.hf_model_id,
            api_token=self.config.hf_api_token,
            temperature=self.config.llm_temperature,
            max_tokens=self.config.llm_max_tokens,
            require_real_llm=self.config.require_real_llm,
        )
        self.llm_info = llm_diagnostics(self.llm)
        self.vector_store = ArtifactVectorStore(
            self.config.vector_db_dir, enable_chromadb=self.config.use_chromadb
        )

        self.business_analyst = BusinessAnalystAgent(
            name="Business Analyst Agent",
            llm=self.llm,
            template_repository=self.template_repository,
            knowledge_dir=self.config.knowledge_dir,
        )
        self.developer = DeveloperAgent(
            name="Developer Agent",
            llm=self.llm,
            template_repository=self.template_repository,
            knowledge_dir=self.config.knowledge_dir,
        )
        self.designer = DesignAgent(
            name="Design Agent",
            llm=self.llm,
            template_repository=self.template_repository,
            knowledge_dir=self.config.knowledge_dir,
        )
        self.tester = TestingAgent(
            name="Testing Agent",
            llm=self.llm,
            template_repository=self.template_repository,
            knowledge_dir=self.config.knowledge_dir,
        )
        self.product_manager = ProductManagerAgent(
            name="Product Manager Agent",
            llm=self.llm,
            template_repository=self.template_repository,
            knowledge_dir=self.config.knowledge_dir,
        )
        self.crewai_planner = CrewAIPlanner(enabled=self.config.enable_crewai)
        self._last_run: RunResult | None = None

    def run_sdlc(
        self,
        business_requirements: str,
        *,
        project_name: str,
        event_callback: Callable[[dict[str, str]], None] | None = None,
    ) -> RunResult:
        business_requirements = business_requirements.strip()
        if not business_requirements:
            raise ValueError("business_requirements cannot be empty")

        run_id = f"{utc_timestamp()}_{slugify(project_name)}"
        run_dir = self.config.artifact_root / run_id
        analysis_dir = run_dir / "analysis"
        design_dir = run_dir / "design"
        development_dir = run_dir / "development"
        package_dir = development_dir / "generated_app"
        testing_dir = run_dir / "testing"
        tests_dir = testing_dir / "tests"
        reports_dir = run_dir / "reports"
        for path in [analysis_dir, design_dir, package_dir, tests_dir, reports_dir]:
            path.mkdir(parents=True, exist_ok=True)

        run_result = RunResult(
            run_id=run_id,
            project_name=project_name,
            requirements=business_requirements,
            run_dir=run_dir,
            llm_provider=str(self.llm_info.get("provider", "")),
            llm_model_id=str(self.llm_info.get("model_id", "")),
            llm_is_mock=bool(self.llm_info.get("is_mock", False)),
            llm_reason=str(self.llm_info.get("reason", "")),
            stage_status={
                "analysis": "pending",
                "design": "pending",
                "development": "pending",
                "testing": "pending",
                "management": "pending",
            },
        )
        self._emit_event(
            run_result,
            event_callback,
            agent="Orchestrator",
            stage="setup",
            status="in_progress",
            message=(
                f"Initialized run {run_id}. fast_mode={self.config.fast_mode}, "
                f"execute_tests={self.config.execute_tests}, "
                f"use_chromadb={self.config.use_chromadb}"
            ),
        )

        run_result.crew_notes = self.crewai_planner.create_handoff_plan(
            business_requirements
        )
        self._emit_event(
            run_result,
            event_callback,
            agent="Orchestrator",
            stage="setup",
            status="completed",
            message="Initial handoff plan prepared.",
        )

        run_result.stage_status["analysis"] = "in_progress"
        self._emit_event(
            run_result,
            event_callback,
            agent="Business Analyst Agent",
            stage="analysis",
            status="in_progress",
            message="Analyzing business requirements and drafting user stories.",
        )
        stories = self.business_analyst.analyze_requirements(
            business_requirements, max_user_stories=self.config.max_user_stories
        )
        user_stories_markdown = self.business_analyst.render_user_stories(stories)
        user_stories_file = analysis_dir / "user_stories.md"
        user_stories_file.write_text(user_stories_markdown, encoding="utf-8")
        run_result.user_stories = stories
        run_result.stage_status["analysis"] = "completed"
        self._emit_event(
            run_result,
            event_callback,
            agent="Business Analyst Agent",
            stage="analysis",
            status="completed",
            message=f"Generated {len(stories)} user stories.",
        )

        run_result.stage_status["design"] = "in_progress"
        self._emit_event(
            run_result,
            event_callback,
            agent="Design Agent",
            stage="design",
            status="in_progress",
            message="Creating design specifications from user stories.",
        )
        design_artifacts = self.designer.create_design_artifacts(
            stories, output_dir=design_dir
        )
        run_result.design_artifacts = design_artifacts
        design_context_by_story = {
            artifact.story_id: artifact.file_path.read_text(encoding="utf-8")
            for artifact in design_artifacts
            if artifact.file_path.exists()
        }
        run_result.stage_status["design"] = "completed"
        self._emit_event(
            run_result,
            event_callback,
            agent="Design Agent",
            stage="design",
            status="completed",
            message=f"Generated {len(design_artifacts)} design artifacts.",
        )

        run_result.stage_status["development"] = "in_progress"
        self._emit_event(
            run_result,
            event_callback,
            agent="Developer Agent",
            stage="development",
            status="in_progress",
            message="Generating implementation modules using design context.",
        )
        code_artifacts = self.developer.build_modules(
            stories,
            output_dir=package_dir,
            design_context_by_story=design_context_by_story,
        )
        run_result.code_artifacts = code_artifacts
        run_result.stage_status["development"] = "completed"
        self._emit_event(
            run_result,
            event_callback,
            agent="Developer Agent",
            stage="development",
            status="completed",
            message=f"Generated {len(code_artifacts)} code modules.",
        )

        run_result.stage_status["testing"] = "in_progress"
        self._emit_event(
            run_result,
            event_callback,
            agent="Testing Agent",
            stage="testing",
            status="in_progress",
            message=(
                "Building test assets "
                + ("(fast-mode templates)." if self.config.fast_mode else "(LLM-enhanced).")
            ),
        )
        test_artifacts = self.tester.build_tests(
            stories=stories,
            code_artifacts=code_artifacts,
            tests_dir=tests_dir,
            package_name="generated_app",
            llm_enhanced=not self.config.fast_mode,
        )
        if self.config.execute_tests:
            test_execution = self.tester.execute_tests(
                run_dir=run_dir, tests_dir=tests_dir, reports_dir=reports_dir
            )
            test_msg = (
                f"Executed tests: passed={test_execution.passed}, "
                f"failed={test_execution.failed}, skipped={test_execution.skipped}."
            )
        else:
            test_execution = None
            test_msg = "Test execution skipped by configuration (VDP_EXECUTE_TESTS=false)."
        run_result.test_artifacts = test_artifacts
        run_result.test_execution = test_execution
        run_result.stage_status["testing"] = "completed"
        self._emit_event(
            run_result,
            event_callback,
            agent="Testing Agent",
            stage="testing",
            status="completed",
            message=f"Generated {len(test_artifacts)} test modules. {test_msg}",
        )

        run_result.stage_status["management"] = "in_progress"
        self._emit_event(
            run_result,
            event_callback,
            agent="Product Manager Agent",
            stage="management",
            status="in_progress",
            message="Reviewing artifacts for status, quality, and completeness.",
        )
        pm_summary_file = reports_dir / "product_manager_summary.md"
        run_result.pm_summary = self.product_manager.summarize_run(run_result)
        pm_summary_file.write_text(run_result.pm_summary, encoding="utf-8")
        run_result.stage_status["management"] = "completed"
        self._emit_event(
            run_result,
            event_callback,
            agent="Product Manager Agent",
            stage="management",
            status="completed",
            message="Generated PM summary and workflow gap analysis.",
        )

        self._index_artifacts(
            run_result=run_result,
            user_stories_file=user_stories_file,
            pm_summary_file=pm_summary_file,
        )

        metadata_path = run_dir / "run_metadata.json"
        run_result.metadata_path = metadata_path
        metadata_path.write_text(
            json.dumps(run_result.to_dict(), indent=2, ensure_ascii=True),
            encoding="utf-8",
        )
        self._emit_event(
            run_result,
            event_callback,
            agent="Orchestrator",
            stage="finalize",
            status="completed",
            message="Run completed and artifacts indexed.",
        )

        self._last_run = run_result
        return run_result

    def pm_chat(self, query: str, *, run_id: str | None = None) -> str:
        if self._last_run is None:
            return "No run is available yet. Execute run_sdlc first."
        if run_id and self._last_run.run_id != run_id:
            return (
                f"Latest run is `{self._last_run.run_id}`. "
                "Load that run or execute a new one before querying."
            )
        try:
            return self.product_manager.answer_query(
                query=query,
                run_result=self._last_run,
                vector_store=self.vector_store,
                top_k=self.config.top_k_context,
            )
        except Exception:
            return self.product_manager.summarize_run(self._last_run)

    def _index_artifacts(
        self,
        *,
        run_result: RunResult,
        user_stories_file: Path,
        pm_summary_file: Path | None = None,
    ) -> None:
        run_id = run_result.run_id
        indexed: list[str] = []

        self.vector_store.index_file(
            file_path=user_stories_file, artifact_type="user_stories", run_id=run_id
        )
        indexed.append(str(user_stories_file))

        for design in run_result.design_artifacts:
            self.vector_store.index_file(
                file_path=design.file_path, artifact_type="design", run_id=run_id
            )
            indexed.append(str(design.file_path))

        for code in run_result.code_artifacts:
            self.vector_store.index_file(
                file_path=code.file_path, artifact_type="code", run_id=run_id
            )
            indexed.append(str(code.file_path))

        for test in run_result.test_artifacts:
            self.vector_store.index_file(
                file_path=test.file_path, artifact_type="unit_test", run_id=run_id
            )
            indexed.append(str(test.file_path))

        if run_result.test_execution is not None:
            self.vector_store.index_file(
                file_path=run_result.test_execution.report_path,
                artifact_type="test_report",
                run_id=run_id,
            )
            indexed.append(str(run_result.test_execution.report_path))
            self.vector_store.index_file(
                file_path=run_result.test_execution.bug_summary_path,
                artifact_type="bug_summary",
                run_id=run_id,
            )
            indexed.append(str(run_result.test_execution.bug_summary_path))

        if pm_summary_file is not None:
            self.vector_store.index_file(
                file_path=pm_summary_file,
                artifact_type="pm_summary",
                run_id=run_id,
            )
            indexed.append(str(pm_summary_file))

        run_result.indexed_artifacts = indexed

    def _emit_event(
        self,
        run_result: RunResult,
        event_callback: Callable[[dict[str, str]], None] | None,
        *,
        agent: str,
        stage: str,
        status: str,
        message: str,
    ) -> None:
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        log_line = f"[{timestamp}] [{agent}] ({stage}) {status}: {message}"
        run_result.agent_logs.append(log_line)
        if event_callback is None:
            return
        payload = {
            "timestamp": timestamp,
            "agent": agent,
            "stage": stage,
            "status": status,
            "message": message,
            "log": log_line,
        }
        try:
            event_callback(payload)
        except Exception:
            return
