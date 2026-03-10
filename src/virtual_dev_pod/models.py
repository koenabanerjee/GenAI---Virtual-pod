from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class UserStory:
    story_id: str
    title: str
    persona: str
    goal: str
    benefit: str
    acceptance_criteria: list[str]
    priority: str = "Medium"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CodeArtifact:
    story_id: str
    module_name: str
    file_path: Path
    summary: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["file_path"] = str(self.file_path)
        return payload


@dataclass
class DesignArtifact:
    story_id: str
    component_name: str
    file_path: Path
    summary: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["file_path"] = str(self.file_path)
        return payload


@dataclass
class TestArtifact:
    story_id: str
    test_name: str
    file_path: Path
    coverage_focus: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["file_path"] = str(self.file_path)
        return payload


@dataclass
class TestExecutionResult:
    return_code: int
    passed: int
    failed: int
    skipped: int
    stdout: str
    stderr: str
    report_path: Path
    bug_summary_path: Path

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["report_path"] = str(self.report_path)
        payload["bug_summary_path"] = str(self.bug_summary_path)
        return payload


@dataclass
class RunResult:
    run_id: str
    project_name: str
    requirements: str
    run_dir: Path
    user_stories: list[UserStory] = field(default_factory=list)
    design_artifacts: list[DesignArtifact] = field(default_factory=list)
    code_artifacts: list[CodeArtifact] = field(default_factory=list)
    test_artifacts: list[TestArtifact] = field(default_factory=list)
    test_execution: TestExecutionResult | None = None
    stage_status: dict[str, str] = field(default_factory=dict)
    crew_notes: str = ""
    llm_provider: str = ""
    llm_model_id: str = ""
    llm_is_mock: bool = False
    llm_reason: str = ""
    agent_logs: list[str] = field(default_factory=list)
    indexed_artifacts: list[str] = field(default_factory=list)
    metadata_path: Path | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "project_name": self.project_name,
            "requirements": self.requirements,
            "run_dir": str(self.run_dir),
            "user_stories": [story.to_dict() for story in self.user_stories],
            "design_artifacts": [
                artifact.to_dict() for artifact in self.design_artifacts
            ],
            "code_artifacts": [artifact.to_dict() for artifact in self.code_artifacts],
            "test_artifacts": [artifact.to_dict() for artifact in self.test_artifacts],
            "test_execution": self.test_execution.to_dict()
            if self.test_execution
            else None,
            "stage_status": self.stage_status,
            "crew_notes": self.crew_notes,
            "llm_provider": self.llm_provider,
            "llm_model_id": self.llm_model_id,
            "llm_is_mock": self.llm_is_mock,
            "llm_reason": self.llm_reason,
            "agent_logs": self.agent_logs,
            "indexed_artifacts": self.indexed_artifacts,
            "metadata_path": str(self.metadata_path) if self.metadata_path else None,
        }
