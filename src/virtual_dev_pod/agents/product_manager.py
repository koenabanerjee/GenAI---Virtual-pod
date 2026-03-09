from __future__ import annotations

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
        context_snippets = []
        for hit in hits:
            path = hit.metadata.get("path", "unknown")
            snippet = trim_words(hit.content.replace("\n", " "), max_words=45)
            context_snippets.append(f"- Source: {path}\n  Snippet: {snippet}")

        summary = self.summarize_run(run_result)
        missing_steps = self.identify_missing_steps(run_result)
        prompt = f"""
You are a Product Manager chatbot supervising the AI development pod.
Answer based on project status and artifacts.
Include concise status, quality, completeness, and missing steps.

Run summary:
{summary}

Relevant artifact context:
{chr(10).join(context_snippets) if context_snippets else "- No matching artifact context."}

Missing steps:
{self._format_missing(missing_steps)}

User question:
{query}
"""
        llm_answer = ""
        try:
            llm_answer = self._call_llm(prompt).strip()
        except Exception:
            llm_answer = ""

        if llm_answer and llm_answer != "MOCK_PROVIDER_ACTIVE":
            return llm_answer

        fallback = [
            f"Run `{run_result.run_id}` status overview:",
            "Stage status:",
        ]
        fallback.extend(
            f"- {stage}: {status}" for stage, status in run_result.stage_status.items()
        )
        fallback.append("Quality and completeness by stage:")
        fallback.extend(self._stage_quality_and_completeness(run_result).splitlines())
        fallback.append("Missing steps:")
        fallback.append(self._format_missing(missing_steps))
        if context_snippets:
            fallback.append("Relevant artifacts:")
            fallback.extend(context_snippets[:3])
        return "\n".join(fallback)

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
