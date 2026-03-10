from __future__ import annotations

import os
import sys
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from typing import Any

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from virtual_dev_pod.workflow import VirtualDevelopmentPod  # noqa: E402


st.set_page_config(page_title="Virtual Development Pod", layout="wide")
st.title("AI-Powered Virtual Development Pod")
st.caption("Multi-agent SDLC automation: BA -> Design -> DEV -> QA -> PM")

STAGE_PROGRESS = {
    "analysis": 20,
    "design": 40,
    "development": 65,
    "testing": 85,
    "management": 100,
}


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _default_stage_status() -> dict[str, str]:
    return {stage: "pending" for stage in STAGE_PROGRESS}


def _progress_from_status(stage_status: dict[str, str]) -> int:
    progress = 0
    for stage, pct in STAGE_PROGRESS.items():
        status = stage_status.get(stage, "pending")
        if status == "completed":
            progress = max(progress, pct)
        elif status == "in_progress":
            progress = max(progress, max(pct - 10, 5))
    return progress


def _try_init_pod() -> tuple[VirtualDevelopmentPod | None, str]:
    try:
        return VirtualDevelopmentPod(), ""
    except Exception as exc:
        return None, str(exc)


def _drain_run_events() -> None:
    event_queue = st.session_state.get("run_event_queue")
    if event_queue is None:
        return

    while True:
        try:
            item = event_queue.get_nowait()
        except Empty:
            break

        event_type = item.get("type", "")
        if event_type == "event":
            event = item.get("event", {})
            if not isinstance(event, dict):
                continue
            log_line = str(event.get("log", "")).strip()
            if log_line:
                st.session_state.agent_activity.append(log_line)
            stage = str(event.get("stage", "")).strip()
            status = str(event.get("status", "")).strip()
            if stage in st.session_state.live_stage_status and status:
                st.session_state.live_stage_status[stage] = status

        elif event_type == "result":
            run_result = item.get("result")
            st.session_state.run_result = run_result
            st.session_state.run_in_progress = False
            st.session_state.run_error = ""
            if run_result is not None and hasattr(run_result, "stage_status"):
                st.session_state.live_stage_status = dict(run_result.stage_status)

        elif event_type == "error":
            error = str(item.get("error", "Unknown run error"))
            st.session_state.run_in_progress = False
            st.session_state.run_error = error
            pod = st.session_state.get("pod")
            if pod is not None:
                pod.mark_live_run_finished(error=error)

    run_thread = st.session_state.get("run_thread")
    if run_thread is not None and not run_thread.is_alive() and not st.session_state.run_in_progress:
        st.session_state.run_thread = None
        st.session_state.run_event_queue = None


def _start_run(requirements: str, project_name: str) -> None:
    pod = st.session_state.pod
    if pod is None:
        return

    if st.session_state.run_in_progress:
        return

    event_queue: Queue[dict[str, Any]] = Queue()
    st.session_state.run_event_queue = event_queue
    st.session_state.run_thread = None
    st.session_state.run_in_progress = True
    st.session_state.run_error = ""
    st.session_state.run_result = None
    st.session_state.chat_history = []
    st.session_state.agent_activity = []
    st.session_state.live_stage_status = _default_stage_status()

    def on_event(event: dict[str, str]) -> None:
        event_queue.put({"type": "event", "event": event})

    def worker() -> None:
        try:
            result = pod.run_sdlc(
                requirements,
                project_name=project_name,
                event_callback=on_event,
            )
            event_queue.put({"type": "result", "result": result})
        except Exception as exc:
            pod.mark_live_run_finished(error=str(exc))
            event_queue.put({"type": "error", "error": str(exc)})

    thread = Thread(target=worker, daemon=True)
    st.session_state.run_thread = thread
    thread.start()


def _local_live_pm_reply() -> str:
    lines = ["SDLC run is active. Current stage status:"]
    lines.extend(
        f"- {stage}: {status}"
        for stage, status in st.session_state.live_stage_status.items()
    )
    if st.session_state.agent_activity:
        lines.append("Recent activity:")
        lines.extend(f"- {line}" for line in st.session_state.agent_activity[-5:])
    return "\n".join(lines)


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
if "run_thread" not in st.session_state:
    st.session_state.run_thread = None
if "run_event_queue" not in st.session_state:
    st.session_state.run_event_queue = None
if "run_in_progress" not in st.session_state:
    st.session_state.run_in_progress = False
if "run_error" not in st.session_state:
    st.session_state.run_error = ""
if "live_stage_status" not in st.session_state:
    st.session_state.live_stage_status = _default_stage_status()

_drain_run_events()

with st.sidebar:
    st.subheader("LLM Settings")
    llm_provider = st.selectbox(
        "Provider",
        options=["langchain_hf_endpoint", "langchain_hf_local", "mock"],
        index=0,
    )
    llm_model_id = st.text_input(
        "Model ID",
        value=os.getenv("VDP_HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2"),
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
        if st.session_state.run_in_progress:
            st.warning("Cannot apply new settings while an SDLC run is in progress.")
        else:
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
            st.session_state.live_stage_status = _default_stage_status()

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
    run_button_disabled = st.session_state.run_in_progress
    if st.button("Run End-to-End SDLC", type="primary", disabled=run_button_disabled):
        if st.session_state.pod is None:
            st.error(f"Pod initialization failed: {st.session_state.pod_error}")
        else:
            _start_run(requirements, project_name)
            st.rerun()

    if st.session_state.run_in_progress:
        st.info("SDLC run is active. You can use the PM chatbot now.")
    if st.button("Refresh Live Status"):
        st.rerun()

with right:
    st.subheader("Stage Status")
    current_stage_status = (
        st.session_state.live_stage_status
        if st.session_state.run_in_progress
        else st.session_state.run_result.stage_status
        if st.session_state.run_result is not None
        else _default_stage_status()
    )
    for stage, status in current_stage_status.items():
        st.write(f"- `{stage}`: **{status}**")
    st.progress(_progress_from_status(current_stage_status))

    if st.session_state.run_result is not None:
        run_result = st.session_state.run_result
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

if st.session_state.run_error:
    st.error(f"Run failed: {st.session_state.run_error}")

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

user_prompt = st.chat_input("Ask PM about progress, quality, risks, or artifacts...")
if user_prompt:
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    if st.session_state.pod is None:
        answer = f"Pod initialization failed: {st.session_state.pod_error}"
    else:
        answer = st.session_state.pod.pm_chat(user_prompt)
        if (
            st.session_state.run_in_progress
            and answer == "No run is available yet. Execute run_sdlc first."
        ):
            answer = _local_live_pm_reply()

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
