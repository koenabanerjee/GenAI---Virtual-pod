from __future__ import annotations

import os
import re
import subprocess
import sys
import traceback
from importlib import util
from pathlib import Path

from virtual_dev_pod.agents.base import BaseAgent
from virtual_dev_pod.models import CodeArtifact, TestArtifact, TestExecutionResult, UserStory


class TestingAgent(BaseAgent):
    def build_tests(
        self,
        *,
        stories: list[UserStory],
        code_artifacts: list[CodeArtifact],
        tests_dir: Path,
        package_name: str = "generated_app",
        llm_enhanced: bool = True,
    ) -> list[TestArtifact]:
        tests_dir.mkdir(parents=True, exist_ok=True)
        artifacts: list[TestArtifact] = []

        story_by_id = {story.story_id: story for story in stories}
        for code in code_artifacts:
            story = story_by_id.get(code.story_id)
            if story is None:
                continue

            test_file = tests_dir / f"test_{code.module_name}.py"
            markdown_case = tests_dir / f"{code.module_name}_test_cases.md"

            if llm_enhanced:
                test_code = self._generate_unit_test_code(
                    story=story,
                    package_name=package_name,
                    module_name=code.module_name,
                )
            else:
                test_code = self.template_repository.render(
                    "unit_test_template.py.tmpl",
                    package_name=package_name,
                    module_name=code.module_name,
                )
            test_file.write_text(test_code, encoding="utf-8")

            if llm_enhanced:
                markdown = self._generate_test_case_markdown(
                    story=story, module_name=code.module_name
                )
            else:
                markdown = self.template_repository.render(
                    "test_case_template.md",
                    story_id=story.story_id,
                    story_title=story.title,
                    module_name=code.module_name,
                    acceptance_criteria="\n".join(
                        f"- {item}" for item in story.acceptance_criteria
                    ),
                )
            markdown_case.write_text(markdown, encoding="utf-8")

            artifacts.append(
                TestArtifact(
                    story_id=story.story_id,
                    test_name=f"test_{code.module_name}",
                    file_path=test_file,
                    coverage_focus=story.goal,
                )
            )

        integration_path = tests_dir / "test_integration_generated_app.py"
        integration_path.write_text(
            self._build_integration_test(
                stories=stories,
                code_artifacts=code_artifacts,
                package_name=package_name,
                llm_enhanced=llm_enhanced,
            ),
            encoding="utf-8",
        )

        return artifacts

    def execute_tests(
        self, *, run_dir: Path, tests_dir: Path, reports_dir: Path
    ) -> TestExecutionResult:
        reports_dir.mkdir(parents=True, exist_ok=True)
        import_path = str(run_dir / "development")
        if _pytest_available():
            command = [sys.executable, "-m", "pytest", "-q", str(tests_dir)]
            env = dict(os.environ)
            env["PYTHONPATH"] = _join_pythonpath(
                import_path, existing=env.get("PYTHONPATH", "")
            )
            result = subprocess.run(
                command,
                cwd=str(run_dir),
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            passed = _extract_count(result.stdout, "passed")
            failed = _extract_count(result.stdout, "failed")
            skipped = _extract_count(result.stdout, "skipped")
            stdout = result.stdout
            stderr = result.stderr
            return_code = result.returncode
        else:
            command = [sys.executable, "<builtin-test-runner>", str(tests_dir)]
            fallback = _run_builtin_tests(
                run_dir=run_dir, tests_dir=tests_dir, import_path=import_path
            )
            passed = fallback["passed"]
            failed = fallback["failed"]
            skipped = 0
            stdout = fallback["stdout"]
            stderr = fallback["stderr"]
            return_code = 0 if failed == 0 else 1

        report_path = reports_dir / "test_report.md"
        bug_summary_path = reports_dir / "bug_summary.md"

        report_body = self._build_test_report(command, stdout, stderr, return_code)
        report_path.write_text(report_body, encoding="utf-8")

        bug_summary = self._build_bug_summary(stdout, stderr, return_code)
        bug_summary_path.write_text(bug_summary, encoding="utf-8")

        return TestExecutionResult(
            return_code=return_code,
            passed=passed,
            failed=failed,
            skipped=skipped,
            stdout=stdout,
            stderr=stderr,
            report_path=report_path,
            bug_summary_path=bug_summary_path,
        )

    def _build_integration_test(
        self,
        *,
        stories: list[UserStory],
        code_artifacts: list[CodeArtifact],
        package_name: str,
        llm_enhanced: bool = True,
    ) -> str:
        if not llm_enhanced:
            return self._build_integration_test_fallback(
                stories=stories, code_artifacts=code_artifacts, package_name=package_name
            )

        prompt = f"""
You are a QA Engineer.
Generate a Python integration test file for these modules:
{chr(10).join(f"- {artifact.module_name}" for artifact in code_artifacts)}

Test requirements:
- import each `build_<module_name>` function from `{package_name}`
- create one integration test named `test_generated_app_integration`
- validate each call returns a dict with keys `story_id` and `status`
- use plain pytest style

Return Python code only.
"""
        llm_output = self._call_llm(prompt)
        llm_code = _extract_python(llm_output)
        if _looks_like_pytest(llm_code) and "test_generated_app_integration" in llm_code:
            return llm_code

        return self._build_integration_test_fallback(
            stories=stories, code_artifacts=code_artifacts, package_name=package_name
        )

    def _build_integration_test_fallback(
        self,
        *,
        stories: list[UserStory],
        code_artifacts: list[CodeArtifact],
        package_name: str,
    ) -> str:
        _ = stories

        imports = "\n".join(
            f"from {package_name}.{artifact.module_name} import build_{artifact.module_name}"
            for artifact in code_artifacts
        )
        calls = "\n".join(
            [
                f"    result_{idx} = build_{artifact.module_name}({{'input': 'sample'}})\n"
                f"    assert isinstance(result_{idx}, dict)"
                for idx, artifact in enumerate(code_artifacts, start=1)
            ]
        )
        if not imports:
            imports = "# No generated modules found"
            calls = "    assert True"
        return f'''"""Integration tests for generated modules."""\n\n{imports}\n\n\ndef test_generated_app_integration():\n{calls}\n'''

    def _generate_unit_test_code(
        self, *, story: UserStory, package_name: str, module_name: str
    ) -> str:
        fallback = self.template_repository.render(
            "unit_test_template.py.tmpl",
            package_name=package_name,
            module_name=module_name,
        )
        prompt = f"""
You are a QA Automation Engineer.
Generate robust pytest unit tests for module `{package_name}.{module_name}`.
User story:
- ID: {story.story_id}
- Title: {story.title}
- Goal: {story.goal}
- Acceptance Criteria:
{chr(10).join(f"- {item}" for item in story.acceptance_criteria)}

Requirements:
- Test module import.
- Test `build_{module_name}` output contract.
- Add at least one assertion tied to acceptance criteria.
- Return Python code only.
"""
        llm_output = self._call_llm(prompt)
        llm_code = _extract_python(llm_output)
        if _looks_like_pytest(llm_code) and f"build_{module_name}" in llm_code:
            return llm_code
        return fallback

    def _generate_test_case_markdown(self, *, story: UserStory, module_name: str) -> str:
        fallback = self.template_repository.render(
            "test_case_template.md",
            story_id=story.story_id,
            story_title=story.title,
            module_name=module_name,
            acceptance_criteria="\n".join(
                f"- {item}" for item in story.acceptance_criteria
            ),
        )
        prompt = f"""
You are a QA Analyst.
Write a markdown test-case document for this story:
- Story ID: {story.story_id}
- Story Title: {story.title}
- Target Module: {module_name}
- Acceptance Criteria:
{chr(10).join(f"- {item}" for item in story.acceptance_criteria)}

Return markdown only with sections:
1) Objective
2) Preconditions
3) Test Cases (tabular or bullet form)
4) Exit Criteria
"""
        llm_output = self._call_llm(prompt).strip()
        if llm_output and llm_output != "MOCK_PROVIDER_ACTIVE":
            return llm_output
        return fallback

    def _build_test_report(
        self, command: list[str], stdout: str, stderr: str, return_code: int
    ) -> str:
        return f"""# Test Execution Report

## Command
`{' '.join(command)}`

## Return Code
{return_code}

## Stdout
```text
{stdout.strip()}
```

## Stderr
```text
{stderr.strip()}
```
"""

    def _build_bug_summary(self, stdout: str, stderr: str, return_code: int) -> str:
        if return_code == 0:
            return self.template_repository.render(
                "bug_report_template.md",
                status="PASS",
                summary="No defects detected. All automated tests passed.",
                details="- No failing tests.",
            )

        detail_lines: list[str] = []
        for line in (stdout + "\n" + stderr).splitlines():
            if "FAILED" in line or "ERROR" in line or line.strip().startswith("E   "):
                detail_lines.append(f"- {line.strip()}")
        if not detail_lines:
            detail_lines = ["- Tests failed; inspect full report for details."]

        return self.template_repository.render(
            "bug_report_template.md",
            status="FAIL",
            summary="Automated tests found defects.",
            details="\n".join(detail_lines[:20]),
        )


def _extract_count(text: str, label: str) -> int:
    match = re.search(rf"(\d+)\s+{label}", text)
    if not match:
        return 0
    return int(match.group(1))


def _pytest_available() -> bool:
    return util.find_spec("pytest") is not None


def _run_builtin_tests(
    *, run_dir: Path, tests_dir: Path, import_path: str
) -> dict[str, int | str]:
    passed = 0
    failed = 0
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    if str(run_dir) not in sys.path:
        sys.path.insert(0, str(run_dir))
    if import_path not in sys.path:
        sys.path.insert(0, import_path)

    for test_file in sorted(tests_dir.glob("test_*.py")):
        spec = util.spec_from_file_location(test_file.stem, test_file)
        if spec is None or spec.loader is None:
            failed += 1
            stderr_lines.append(f"Unable to load test module: {test_file}")
            continue
        module = util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)  # type: ignore[attr-defined]
        except Exception:
            failed += 1
            stderr_lines.append(f"Failed importing {test_file.name}")
            stderr_lines.append(traceback.format_exc())
            continue

        test_functions = [
            getattr(module, name)
            for name in dir(module)
            if name.startswith("test_") and callable(getattr(module, name))
        ]
        for fn in test_functions:
            try:
                fn()
                passed += 1
                stdout_lines.append(f"PASS {test_file.name}::{fn.__name__}")
            except Exception:
                failed += 1
                stderr_lines.append(f"FAIL {test_file.name}::{fn.__name__}")
                stderr_lines.append(traceback.format_exc())

    stdout_lines.append(
        f"summary: {passed} passed, {failed} failed (builtin-test-runner)"
    )
    return {
        "passed": passed,
        "failed": failed,
        "stdout": "\n".join(stdout_lines).strip(),
        "stderr": "\n".join(stderr_lines).strip(),
    }


def _join_pythonpath(import_path: str, *, existing: str = "") -> str:
    if existing:
        return f"{import_path}{os.pathsep}{existing}"
    return import_path


def _extract_python(text: str) -> str:
    if not text:
        return ""
    fenced_python = re.findall(
        r"```python\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE
    )
    if fenced_python:
        return fenced_python[0].strip() + "\n"
    fenced_any = re.findall(r"```\s*(.*?)```", text, flags=re.DOTALL)
    if fenced_any:
        return fenced_any[0].strip() + "\n"
    return text.strip() + "\n"


def _looks_like_pytest(text: str) -> bool:
    if not text.strip():
        return False
    return "def test_" in text and "assert " in text
