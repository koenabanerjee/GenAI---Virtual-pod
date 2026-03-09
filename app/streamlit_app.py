from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from virtual_dev_pod.workflow import VirtualDevelopmentPod  # noqa: E402


st.set_page_config(page_title="Virtual Development Pod", layout="wide")
st.title("AI-Powered Virtual Development Pod")
st.caption("Multi-agent SDLC automation: BA -> Design -> DEV -> QA -> PM")


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _try_init_pod() -> tuple[VirtualDevelopmentPod | None, str]:
    try:
        return VirtualDevelopmentPod(), ""
    except Exception as exc:
        return None, str(exc)


with st.sidebar:
    st.subheader("LLM Settings")
    llm_provider = st.selectbox(
        "Provider",
        options=["langchain_hf_endpoint", "langchain_hf_local", "mock"],
        index=0,
    )
    llm_model_id = st.text_input(
        "Model ID", value=os.getenv("VDP_HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2")
    )
    hf_token = st.text_input(
        "HF API Token (for endpoint mode)",
        type="password",
        value=os.getenv("HUGGINGFACEHUB_API_TOKEN", ""),
    )
    require_real_llm = st.checkbox("Require Real LLM", value=True)
    st.subheader("Execution Settings")
    fast_mode = st.checkbox(
        "Fast Mode (reduced latency)",
        value=_bool_env("VDP_FAST_MODE", True),
    )
    execute_tests = st.checkbox(
        "Execute Tests",
        value=_bool_env("VDP_EXECUTE_TESTS", True),
    )
    use_chromadb = st.checkbox(
        "Use ChromaDB Embeddings",
        value=_bool_env("VDP_USE_CHROMADB", False),
    )
    max_user_stories = st.slider(
        "Max User Stories",
        min_value=1,
        max_value=8,
        value=int(os.getenv("VDP_MAX_USER_STORIES", "5")),
    )

    if st.button("Apply LLM Settings"):
        os.environ["VDP_LLM_PROVIDER"] = llm_provider
        os.environ["VDP_HF_MODEL_ID"] = llm_model_id
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
        os.environ["VDP_REQUIRE_REAL_LLM"] = "true" if require_real_llm else "false"
        os.environ["VDP_FAST_MODE"] = "true" if fast_mode else "false"
        os.environ["VDP_EXECUTE_TESTS"] = "true" if execute_tests else "false"
        os.environ["VDP_USE_CHROMADB"] = "true" if use_chromadb else "false"
        os.environ["VDP_MAX_USER_STORIES"] = str(max_user_stories)
        st.session_state.pod, st.session_state.pod_error = _try_init_pod()
        st.session_state.run_result = None
        st.session_state.chat_history = []
        st.session_state.agent_activity = []

if "pod" not in st.session_state:
    st.session_state.pod, st.session_state.pod_error = _try_init_pod()
if "run_result" not in st.session_state:
    st.session_state.run_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pod_error" not in st.session_state:
    st.session_state.pod_error = ""
if "agent_activity" not in st.session_state:
    st.session_state.agent_activity = []

left, right = st.columns([3, 2])

with left:
    project_name = st.text_input("Project Name", value="virtual-development-pod-demo")
    requirements = st.text_area(
        "High-Level Business Requirements",
        height=260,
        value=(
            "Build an AI-enabled virtual development team that receives business "
            "requirements, produces user stories, generates implementation code, "
            "auto-creates tests, executes validation, and reports progress to PM."
        ),
    )
    if st.button("Run End-to-End SDLC", type="primary"):
        if st.session_state.pod is None:
            st.error(f"Pod initialization failed: {st.session_state.pod_error}")
        else:
            st.session_state.agent_activity = []
            status_box = st.status(
                "Running BA, Design, DEV, QA, and PM agents...", expanded=True
            )
            progress_bar = st.progress(0)
            stage_progress = {
                "analysis": 20,
                "design": 40,
                "development": 65,
                "testing": 85,
                "management": 100,
            }

            def on_event(event: dict[str, str]) -> None:
                log_line = event.get("log", "")
                if log_line:
                    st.session_state.agent_activity.append(log_line)
                    status_box.write(log_line)
                stage = event.get("stage", "")
                if event.get("status") == "completed" and stage in stage_progress:
                    progress_bar.progress(stage_progress[stage])

            try:
                st.session_state.run_result = st.session_state.pod.run_sdlc(
                    requirements,
                    project_name=project_name,
                    event_callback=on_event,
                )
                st.session_state.chat_history = []
                progress_bar.progress(100)
                status_box.update(label="Run completed", state="complete")
            except Exception as exc:
                status_box.update(label=f"Run failed: {exc}", state="error")
                st.error(f"Run failed: {exc}")

with right:
    st.subheader("Stage Status")
    run_result = st.session_state.run_result
    if run_result is None:
        st.info("No run yet.")
    else:
        for stage, status in run_result.stage_status.items():
            st.write(f"- `{stage}`: **{status}**")
        st.subheader("Output")
        st.write(f"Run ID: `{run_result.run_id}`")
        st.write(f"Artifacts: `{run_result.run_dir}`")
        if run_result.test_execution:
            st.write(
                "Tests: "
                f"passed={run_result.test_execution.passed}, "
                f"failed={run_result.test_execution.failed}, "
                f"skipped={run_result.test_execution.skipped}"
            )
        if run_result.pm_summary:
            st.subheader("PM Summary")
            st.markdown(run_result.pm_summary)

st.divider()
if st.session_state.pod is None:
    st.error(f"Pod initialization failed: {st.session_state.pod_error}")
else:
    llm_info = st.session_state.pod.llm_info
    st.caption(
        "LLM runtime: "
        f"provider={llm_info.get('provider')} | "
        f"model={llm_info.get('model_id')} | "
        f"mock={llm_info.get('is_mock')}"
    )
    if llm_info.get("is_mock"):
        st.warning(f"Running with mock fallback. Reason: {llm_info.get('reason')}")

st.subheader("Agent Activity")
if st.session_state.agent_activity:
    st.code("\n".join(st.session_state.agent_activity), language="text")
else:
    st.info("No agent activity yet. Run the SDLC workflow to see live steps.")

st.subheader("Product Manager Chatbot")
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Ask PM about progress, quality, or artifacts...")
if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if st.session_state.pod is None:
        answer = f"Pod initialization failed: {st.session_state.pod_error}"
    elif st.session_state.run_result is None:
        answer = "Run the SDLC workflow first to create project artifacts."
    else:
        answer = st.session_state.pod.pm_chat(user_prompt)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
