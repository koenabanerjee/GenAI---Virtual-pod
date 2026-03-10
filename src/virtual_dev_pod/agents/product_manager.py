from __future__ import annotations

import re
from typing import Any

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import RunResult
from virtual_dev_pod.utils import trim_words
from virtual_dev_pod.vector_store import ArtifactVectorStore


class ProductManagerAgent(BaseAgent):
    def summarize_run(self, run_result: RunResult) -> str:
        missing_steps = self.identify_missing_steps(run_result)
        stage_quality = self._stage_quality_and_completeness(run_result)
        stage_lines = "\n".join(
            f"- {stage}: {status}" for stage, status in run_result.stage_status.items()
        )
        return f"""# Product Manager SDLC Summary

Project: {run_result.project_name}
Run ID: {run_result.run_id}

## Stage Status
{stage_lines}

## Artifact Coverage
- User stories (BA): {len(run_result.user_stories)}
- Design specs: {len(run_result.design_artifacts)}
- Code modules (DEV): {len(run_result.code_artifacts)}
- Test files (QA): {len(run_result.test_artifacts)}

## Stage Quality and Completeness
{stage_quality}

## Completeness
{"Complete" if not missing_steps else "Incomplete"}

## Missing Steps
{self._format_missing(missing_steps)}
""".strip()

    def identify_missing_steps(self, run_result: RunResult) -> list[str]:
        missing: list[str] = []
        if not run_result.user_stories:
            missing.append("Business Analyst stage did not produce user stories.")
        if not run_result.code_artifacts:
            missing.append("Developer stage did not produce code modules.")
        if not run_result.test_artifacts:
            missing.append("Testing stage did not produce test files.")
        if run_result.test_execution is None:
            missing.append("Automated test execution report is missing.")
        elif run_result.test_execution.failed > 0:
            missing.append(
                f"Automated tests have failures ({run_result.test_execution.failed} failed)."
            )
        incomplete_stages = [
            stage
            for stage, status in run_result.stage_status.items()
            if status != "completed"
        ]
        for stage in incomplete_stages:
            missing.append(f"Stage `{stage}` is not completed ({run_result.stage_status[stage]}).")
        return missing

    def answer_query(
        self,
        *,
        query: str,
        run_result: RunResult,
        vector_store: ArtifactVectorStore,
        top_k: int = 5,
    ) -> str:
        hits = vector_store.search(
            query, top_k=top_k, metadata_filter={"run_id": run_result.run_id}
        )
        context_snippets = self._format_hits(hits, max_items=5, max_words=45)
        missing_steps = self.identify_missing_steps(run_result)
        lower_query = query.lower()
        stage_focus = self._infer_stage_focus(lower_query)

        if stage_focus:
            stage_logs = self._filter_logs_by_stage(run_result.agent_logs, stage_focus)
            stage_heading = self._stage_label(stage_focus)
            details = self._stage_details_for_completed_run(run_result, stage_focus)
            return "\n".join(
                [
                    f"{stage_heading} update for run `{run_result.run_id}`:",
                    f"- Status: {run_result.stage_status.get(stage_focus, 'unknown')}",
                    f"- {details}",
                    "Recent stage activity:",
                    *self._last_log_lines(stage_logs, max_items=5),
                ]
            )

        if self._matches_any(lower_query, {"risk", "blocker", "dependency", "delay"}):
            lines = [
                f"Risk view for run `{run_result.run_id}`:",
            ]
            if missing_steps:
                lines.append("- Active risks and gaps:")
                lines.extend(f"- {item}" for item in missing_steps[:6])
            else:
                lines.append("- No major risks detected. All stages completed with no open gaps.")
            lines.append("Recent activity:")
            lines.extend(self._last_log_lines(run_result.agent_logs, max_items=6))
            return "\n".join(lines)

        if self._matches_any(lower_query, {"quality", "test", "defect", "bug", "coverage"}):
            lines = [
                f"Quality view for run `{run_result.run_id}`:",
                f"- Testing assessment: {self._test_quality(run_result)}",
            ]
            if run_result.test_execution is not None:
                lines.append(
                    "- Test execution: "
                    f"passed={run_result.test_execution.passed}, "
                    f"failed={run_result.test_execution.failed}, "
                    f"skipped={run_result.test_execution.skipped}"
                )
            else:
                lines.append("- Test execution report is not available.")
            lines.append("Recent QA activity:")
            lines.extend(
                self._last_log_lines(
                    self._filter_logs_by_stage(run_result.agent_logs, "testing"), max_items=5
                )
            )
            return "\n".join(lines)

        if self._matches_any(
            lower_query,
            {
                "artifact",
                "file",
                "module",
                "story",
                "stories",
                "design",
                "code",
                "test case",
                "report",
            },
        ):
            lines = [
                f"Artifact view for run `{run_result.run_id}`:",
                f"- User stories: {len(run_result.user_stories)}",
                f"- Design specs: {len(run_result.design_artifacts)}",
                f"- Code modules: {len(run_result.code_artifacts)}",
                f"- Test files: {len(run_result.test_artifacts)}",
            ]
            if context_snippets:
                lines.append("Top relevant artifacts:")
                lines.extend(context_snippets[:5])
            else:
                lines.append("- No matching artifact context found for this query.")
            return "\n".join(lines)

        if self._matches_any(lower_query, {"missing", "gap", "incomplete", "left"}):
            return "\n".join(
                [
                    f"Completeness view for run `{run_result.run_id}`:",
                    self._format_missing(missing_steps),
                ]
            )

        completed, in_progress, pending = self._split_stage_status(run_result.stage_status)
        lines = [
            f"Progress view for run `{run_result.run_id}`:",
            f"- Completed stages: {', '.join(completed) if completed else 'none'}",
            f"- In progress stages: {', '.join(in_progress) if in_progress else 'none'}",
            f"- Pending stages: {', '.join(pending) if pending else 'none'}",
            "Stage status:",
        ]
        lines.extend(
            f"- {stage}: {status}" for stage, status in run_result.stage_status.items()
        )
        if context_snippets:
            lines.append("Relevant artifacts:")
            lines.extend(context_snippets[:3])
        return "\n".join(lines)

    def answer_live_query(
        self,
        *,
        query: str,
        live_status: dict[str, Any],
        vector_store: ArtifactVectorStore,
        top_k: int = 5,
    ) -> str:
        _ = (vector_store, top_k)
        run_id = str(live_status.get("run_id", "unknown"))
        project_name = str(live_status.get("project_name", "unknown"))
        stage_status = live_status.get("stage_status", {})
        if not isinstance(stage_status, dict):
            stage_status = {}
        agent_logs = live_status.get("agent_logs", [])
        if not isinstance(agent_logs, list):
            agent_logs = []

        completed = [stage for stage, status in stage_status.items() if status == "completed"]
        in_progress = [
            stage for stage, status in stage_status.items() if status == "in_progress"
        ]
        pending = [stage for stage, status in stage_status.items() if status == "pending"]

        lower_query = query.lower()
        stage_focus = self._infer_stage_focus(lower_query)
        if stage_focus:
            stage_logs = self._filter_logs_by_stage(agent_logs, stage_focus)
            return "\n".join(
                [
                    f"{self._stage_label(stage_focus)} live update for run `{run_id}` ({project_name}):",
                    f"- Stage status: {stage_status.get(stage_focus, 'unknown')}",
                    "Recent stage activity:",
                    *self._last_log_lines(stage_logs, max_items=6),
                ]
            )

        if "risk" in lower_query or "blocker" in lower_query:
            risk_line = (
                "No blockers reported in agent logs yet."
                if not pending and not in_progress
                else "Primary risk is unfinished stages: "
                + (", ".join(in_progress + pending) if (in_progress or pending) else "none")
            )
            return "\n".join(
                [
                    f"Live run `{run_id}` ({project_name}) risk view:",
                    risk_line,
                    "Recent activity:",
                    *[f"- {entry}" for entry in agent_logs[-6:]],
                ]
            )

        if "quality" in lower_query or "test" in lower_query:
            return "\n".join(
                [
                    f"Live run `{run_id}` ({project_name}) quality view:",
                    (
                        "- Testing is still in progress; quality metrics are preliminary."
                        if "testing" in in_progress or "testing" in pending
                        else "- Testing stage completed; final quality is available in reports."
                    ),
                    (
                        "- No test execution counts yet."
                        if not any("Executed tests:" in line for line in agent_logs[-10:])
                        else "- Test execution has started producing metrics."
                    ),
                    "Stage status:",
                    *[f"- {stage}: {status}" for stage, status in stage_status.items()],
                    "Recent activity:",
                    *[f"- {entry}" for entry in agent_logs[-6:]],
                ]
            )

        if self._matches_any(
            lower_query,
            {"artifact", "file", "module", "story", "stories", "design", "code", "report"},
        ):
            generated = self._extract_generated_counts(agent_logs)
            return "\n".join(
                [
                    f"Live artifact view for run `{run_id}` ({project_name}):",
                    f"- User stories generated: {generated.get('user_stories', 'pending')}",
                    f"- Design specs generated: {generated.get('design_artifacts', 'pending')}",
                    f"- Code modules generated: {generated.get('code_modules', 'pending')}",
                    f"- Test modules generated: {generated.get('test_modules', 'pending')}",
                    "Recent activity:",
                    *[f"- {entry}" for entry in agent_logs[-6:]],
                ]
            )

        return "\n".join(
            [
                f"Live run `{run_id}` ({project_name}) is in progress.",
                f"- Completed stages: {', '.join(completed) if completed else 'none'}",
                f"- In progress stages: {', '.join(in_progress) if in_progress else 'none'}",
                f"- Pending stages: {', '.join(pending) if pending else 'none'}",
                "Detailed stage status:",
                *[f"- {stage}: {status}" for stage, status in stage_status.items()],
                "Recent activity:",
                *[f"- {entry}" for entry in agent_logs[-6:]],
            ]
        )

    def _infer_stage_focus(self, lower_query: str) -> str | None:
        mapping = {
            "analysis": {"analysis", "business analyst", "ba", "user story", "stories"},
            "design": {"design", "architecture", "spec"},
            "development": {"development", "developer", "dev", "code", "module", "implement"},
            "testing": {"testing", "qa", "test", "bug", "defect"},
            "management": {"pm", "product manager", "management"},
        }
        for stage, keywords in mapping.items():
            if self._matches_any(lower_query, keywords):
                return stage
        return None

    def _stage_label(self, stage: str) -> str:
        labels = {
            "analysis": "Business Analyst",
            "design": "Design",
            "development": "Developer",
            "testing": "Testing",
            "management": "Product Manager",
        }
        return labels.get(stage, stage.capitalize())

    def _stage_details_for_completed_run(self, run_result: RunResult, stage: str) -> str:
        if stage == "analysis":
            stories = len(run_result.user_stories)
            with_ac = sum(1 for s in run_result.user_stories if s.acceptance_criteria)
            return f"Generated {stories} user stories ({with_ac} with acceptance criteria)."
        if stage == "design":
            return f"Generated {len(run_result.design_artifacts)} design artifacts."
        if stage == "development":
            return f"Generated {len(run_result.code_artifacts)} code modules."
        if stage == "testing":
            if run_result.test_execution is None:
                return f"Generated {len(run_result.test_artifacts)} test files; execution report unavailable."
            return (
                f"Generated {len(run_result.test_artifacts)} test files; "
                f"passed={run_result.test_execution.passed}, "
                f"failed={run_result.test_execution.failed}, "
                f"skipped={run_result.test_execution.skipped}."
            )
        return "Monitoring artifacts and stage progression."

    def _split_stage_status(
        self, stage_status: dict[str, str]
    ) -> tuple[list[str], list[str], list[str]]:
        completed = [stage for stage, status in stage_status.items() if status == "completed"]
        in_progress = [
            stage for stage, status in stage_status.items() if status == "in_progress"
        ]
        pending = [stage for stage, status in stage_status.items() if status == "pending"]
        return completed, in_progress, pending

    def _format_hits(self, hits: list[Any], *, max_items: int, max_words: int) -> list[str]:
        lines: list[str] = []
        for hit in hits[:max_items]:
            metadata = getattr(hit, "metadata", {}) or {}
            content = str(getattr(hit, "content", ""))
            path = metadata.get("path", "unknown")
            artifact_type = metadata.get("artifact_type", "artifact")
            snippet = trim_words(content.replace("\n", " "), max_words=max_words)
            lines.append(f"- [{artifact_type}] {path}: {snippet}")
        return lines

    def _matches_any(self, text: str, keywords: set[str]) -> bool:
        return any(token in text for token in keywords)

    def _filter_logs_by_stage(self, logs: list[str], stage: str) -> list[str]:
        token = f"({stage})"
        return [line for line in logs if token in line]

    def _last_log_lines(self, logs: list[str], *, max_items: int) -> list[str]:
        if not logs:
            return ["- No activity logged yet."]
        return [f"- {line}" for line in logs[-max_items:]]

    def _extract_generated_counts(self, logs: list[str]) -> dict[str, str]:
        patterns = {
            "user_stories": r"Generated (\d+) user stories",
            "design_artifacts": r"Generated (\d+) design artifacts",
            "code_modules": r"Generated (\d+) code modules",
            "test_modules": r"Generated (\d+) test modules",
        }
        counts: dict[str, str] = {}
        for key, pattern in patterns.items():
            count = "pending"
            regex = re.compile(pattern, flags=re.IGNORECASE)
            for line in reversed(logs):
                match = regex.search(line)
                if match:
                    count = match.group(1)
                    break
            counts[key] = count
        return counts

    def _test_quality(self, run_result: RunResult) -> str:
        if run_result.test_execution is None:
            return "Test execution not available."
        if run_result.test_execution.failed > 0:
            return (
                "At risk: "
                f"{run_result.test_execution.failed} failed, "
                f"{run_result.test_execution.passed} passed."
            )
        return (
            "Good: "
            f"{run_result.test_execution.passed} passed, "
            f"{run_result.test_execution.failed} failed."
        )

    def _stage_quality_and_completeness(self, run_result: RunResult) -> str:
        stories = len(run_result.user_stories)
        stories_with_ac = sum(
            1 for story in run_result.user_stories if story.acceptance_criteria
        )

        ba_status = "Good" if stories > 0 and stories_with_ac == stories else "At risk"
        dev_status = (
            "Good"
            if stories > 0 and len(run_result.code_artifacts) >= stories
            else "At risk"
        )
        qa_status = "Good" if run_result.test_artifacts else "At risk"

        return "\n".join(
            [
                (
                    f"- Business Analyst: {ba_status} "
                    f"({stories} stories, {stories_with_ac}/{stories} with acceptance criteria)"
                ),
                (
                    f"- Developer: {dev_status} "
                    f"({len(run_result.code_artifacts)} modules for {stories} stories)"
                ),
                (
                    f"- Testing: {qa_status} "
                    f"({len(run_result.test_artifacts)} test files, {self._test_quality(run_result)})"
                ),
            ]
        )

    def _format_missing(self, missing_steps: list[str]) -> str:
        if not missing_steps:
            return "- No missing steps detected."
        return "\n".join(f"- {item}" for item in missing_steps)
