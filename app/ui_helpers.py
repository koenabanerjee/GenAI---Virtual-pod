"""Helper functions for displaying SDLC artifacts in Streamlit UI."""

from pathlib import Path
from typing import Optional

import streamlit as st

from virtual_dev_pod.models import (
    CodeArtifact,
    DesignArtifact,
    RunResult,
    TestArtifact,
    TestExecutionResult,
    UIPageArtifact,
    UserStory,
)

from virtual_dev_pod.utils import slugify


def display_user_stories(stories: list[UserStory], user_stories_file: Optional[Path] = None) -> None:
    """Display user stories in a formatted, expanded view."""
    if not stories:
        st.info("No user stories generated yet.")
        return
    
    for idx, story in enumerate(stories, 1):
        with st.expander(
            f"**{idx}. {story.title}** (ID: {story.story_id})",
            expanded=(idx == 1),
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Persona:** {story.persona}")
                st.write(f"**Priority:** {story.priority}")
            with col2:
                st.write(f"**Goal:** {story.goal}")
                st.write(f"**Benefit:** {story.benefit}")
            
            st.write("**Acceptance Criteria:**")
            for criterion in story.acceptance_criteria:
                st.write(f"- {criterion}")
    
    # Also show user_stories.md file if available
    if user_stories_file and user_stories_file.exists():
        with st.expander("User Stories (Full Markdown)", expanded=False):
            st.markdown(user_stories_file.read_text(encoding="utf-8"))

def display_ui_mockups(
    ui_artifacts: list[UIPageArtifact],
    run_dir: Path,
) -> None:
    """Display UI mockups, specifications, and wireframes.

    When older runs produced a raw page dictionary (without a `pages` key),
    the UI artifacts list in the run metadata would be empty.  In that case
    we attempt to recover by reading and normalizing the legacy
    `pages.json` directly from the run directory.
    """
    if not ui_artifacts:
        # attempt to recover from existing pages.json (legacy format)
        pages_file = run_dir / "ui" / "pages.json"
        if pages_file.exists():
            try:
                import json

                raw = json.loads(pages_file.read_text(encoding="utf-8"))
                # normalization similar to UIDesignerAgent
                if isinstance(raw, dict) and "pages" not in raw:
                    single = raw.copy()
                    raw = {
                        "pages": [
                            {
                                "name": single.get("name"),
                                "story_id": single.get("story_id"),
                                "components": single.get("components", []),
                                "layout": single.get("layout", ""),
                                "description": single.get("description", ""),
                            }
                        ],
                        "navigation": single.get("navigation", ""),
                        "color_scheme": single.get("color_scheme", ""),
                        "typography": single.get("typography", ""),
                    }
                # rebuild ui_artifacts list
                ui_artifacts = []
                for page_info in raw.get("pages", []):
                    story_id = page_info.get("story_id")
                    ui_artifacts.append(
                        UIPageArtifact(
                            page_name=page_info.get("name", "page"),
                            components=page_info.get("components", []),
                            layout_description=page_info.get("layout", ""),
                            story_id=story_id,
                            mockup_path=(
                                run_dir
                                / "ui"
                                / "mockups"
                                / f"{slugify(page_info.get('name', 'page'))}.html"
                            ),
                        )
                    )
            except Exception:
                ui_artifacts = []

    if not ui_artifacts:
        st.info("No UI artifacts generated yet.")
        return
    
    mockups_dir = run_dir / "ui" / "mockups"
    
    # Display UI specification
    ui_spec_file = run_dir / "ui" / "ui_spec.md"
    if ui_spec_file.exists():
        with st.expander("UI Design Specification", expanded=True):
            st.markdown(ui_spec_file.read_text(encoding="utf-8"))
    
    # Display each page mockup
    mockup_tabs = st.tabs([f"{page.page_name}" for page in ui_artifacts])
    
    for tab, page in zip(mockup_tabs, ui_artifacts):
        with tab:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.write("**Components:**")
                for comp in page.components:
                    st.write(f"- {comp}")
            
            with col2:
                st.write("**Layout:**")
                st.write(page.layout_description)
            
            # Display HTML mockup
            html_file = mockups_dir / f"{page.page_name.lower().replace(' ', '_')}.html"
            if html_file.exists():
                with st.expander("Interactive HTML Preview", expanded=True):
                    html_content = html_file.read_text(encoding="utf-8")
                    st.components.v1.html(html_content, height=800, scrolling=True)


def display_design_specifications(design_artifacts: list[DesignArtifact]) -> None:
    """Display architecture and design specifications."""
    if not design_artifacts:
        st.info("No design artifacts generated yet.")
        return
    
    for idx, design in enumerate(design_artifacts, 1):
        with st.expander(
            f"**{idx}. {design.component_name}** (Story: {design.story_id})",
            expanded=(idx == 1),
        ):
            st.write(f"**Summary:** {design.summary}")
            
            # Read and display the design file
            if design.file_path and Path(design.file_path).exists():
                design_content = Path(design.file_path).read_text(encoding="utf-8")
                st.markdown(design_content)
            else:
                st.info(f"Design file not found at {design.file_path}")


def display_generated_code(code_artifacts: list[CodeArtifact]) -> None:
    """Display generated Python source code modules."""
    if not code_artifacts:
        st.info("No code artifacts generated yet.")
        return
    
    code_tabs = st.tabs([f"{code.module_name}" for code in code_artifacts])
    
    for tab, code_artifact in zip(code_tabs, code_artifacts):
        with tab:
            st.write(f"**Story ID:** {code_artifact.story_id}")
            st.write(f"**Summary:** {code_artifact.summary}")
            
            # Read and display code
            if code_artifact.file_path and Path(code_artifact.file_path).exists():
                code_content = Path(code_artifact.file_path).read_text(encoding="utf-8")
                st.code(code_content, language="python")
            else:
                st.warning(f"Code file not found at {code_artifact.file_path}")


def display_generated_tests(test_artifacts: list[TestArtifact]) -> None:
    """Display generated unit and integration tests."""
    if not test_artifacts:
        st.info("No test artifacts generated yet.")
        return
    
    test_tabs = st.tabs([f"{test.test_name}" for test in test_artifacts])
    
    for tab, test_artifact in zip(test_tabs, test_artifacts):
        with tab:
            st.write(f"**Story ID:** {test_artifact.story_id}")
            st.write(f"**Focus:** {test_artifact.coverage_focus}")
            
            # Read and display test code
            if test_artifact.file_path and Path(test_artifact.file_path).exists():
                test_content = Path(test_artifact.file_path).read_text(encoding="utf-8")
                st.code(test_content, language="python")
            else:
                st.warning(f"Test file not found at {test_artifact.file_path}")


def display_test_execution_report(test_execution: TestExecutionResult) -> None:
    """Display test execution results, statistics, and reports."""
    if not test_execution:
        st.info("Tests were not executed. Check settings: VDP_EXECUTE_TESTS=true")
        return
    
    # Test statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Passed", test_execution.passed, delta=None)
    with col2:
        st.metric("Failed", test_execution.failed, delta=None)
    with col3:
        st.metric("Skipped", test_execution.skipped, delta=None)
    with col4:
        status_text = "Success" if test_execution.failed == 0 else "Failed"
        st.metric("Status", status_text, delta=None)
    
    st.divider()
    
    # Test report
    if test_execution.report_path and Path(test_execution.report_path).exists():
        with st.expander("Full Test Report", expanded=True):
            report_content = Path(test_execution.report_path).read_text(encoding="utf-8")
            st.text(report_content)
    
    # Bug summary
    if test_execution.bug_summary_path and Path(test_execution.bug_summary_path).exists():
        with st.expander("Bug Summary", expanded=False):
            bug_content = Path(test_execution.bug_summary_path).read_text(encoding="utf-8")
            st.text(bug_content)
    
    # Test output
    if test_execution.stdout:
        with st.expander("Test Output (stdout)", expanded=False):
            st.code(test_execution.stdout, language="text")
    
    if test_execution.stderr:
        with st.expander("Test Errors (stderr)", expanded=False):
            st.code(test_execution.stderr, language="text")


def display_run_summary(run_result: RunResult) -> None:
    """Display overall SDLC run summary and statistics."""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Run ID", run_result.run_id[:16] + "...")
    with col2:
        st.metric("Project", run_result.project_name)
    with col3:
        st.metric("Status", "Completed")
    
    st.divider()
    st.write("**Run Details:**")
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.write(f"- **User Stories:** {len(run_result.user_stories)}")
        st.write(f"- **Design Artifacts:** {len(run_result.design_artifacts)}")
        st.write(f"- **Code Modules:** {len(run_result.code_artifacts)}")
    
    with detail_col2:
        st.write(f"- **UI Pages:** {len(run_result.ui_artifacts)}")
        st.write(f"- **Test Modules:** {len(run_result.test_artifacts)}")
        if run_result.test_execution:
            total_tests = (
                run_result.test_execution.passed
                + run_result.test_execution.failed
                + run_result.test_execution.skipped
            )
            st.write(f"- **Tests Executed:** {total_tests}")
    
    st.divider()
    st.write("**LLM Configuration:**")
    st.write(f"- Provider: `{run_result.llm_provider}`")
    st.write(f"- Model: `{run_result.llm_model_id}`")
    st.write(f"- Is Mock: `{run_result.llm_is_mock}`")
    if run_result.llm_reason:
        st.write(f"- Reason: `{run_result.llm_reason}`")
    
    st.divider()
    st.write(f"Artifacts saved to: `{run_result.run_dir}`")
