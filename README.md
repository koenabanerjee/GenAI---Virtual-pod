# AI-Powered Virtual Development Pod

This project simulates a real IT delivery team and automates the full SDLC using a multi-agent AI framework.

## What It Does

- Accepts high-level business requirements.
- Runs a role-based pipeline:
  - Business Analyst Agent -> user stories + acceptance criteria.
  - Design Agent -> design specifications and architecture notes.
  - Developer Agent -> Python source modules.
  - Testing Agent -> unit/integration tests + execution + reports.
  - Product Manager Agent -> stage monitoring, quality/completeness checks, and chatbot answers.
- Enforces enterprise-style artifact templates from `org_repository/templates`.
- Stores artifacts in vector memory (ChromaDB when available, local fallback otherwise) for retrieval-augmented PM responses.
- Exposes a Streamlit chatbot dashboard for project leads.
- Captures active LLM mode in run metadata (`provider`, `model`, `mock/fallback status`).
- Shows live agent activity logs during execution in the UI.

## Tech Stack

- Backend: Python
- Multi-agent orchestration: CrewAI (optional adapter) + native pipeline
- LLM integration: LangChain + Hugging Face (optional), with `mock` offline fallback
- Vector DB: ChromaDB (with local searchable fallback)
- UI: Streamlit

## Project Structure

```text
.
|- app/streamlit_app.py
|- examples/sample_requirements.md
|- org_repository/
|  |- knowledge/engineering_standards.md
|  |- templates/
|- src/virtual_dev_pod/
|  |- agents/
|  |- config.py
|  |- crew_adapter.py
|  |- llm_factory.py
|  |- models.py
|  |- repository.py
|  |- vector_store.py
|  |- workflow.py
|- tests/
|- run_pipeline.py
|- requirements.txt
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create environment config:

```bash
cp .env.example .env
```

The `.env.example` is configured for real LangChain + Hugging Face endpoint usage.
Set a valid `HUGGINGFACEHUB_API_TOKEN` before running.

If you want offline fallback behavior, set:

```bash
VDP_LLM_PROVIDER=mock
VDP_REQUIRE_REAL_LLM=false
```

## Run End-to-End SDLC (CLI)

```bash
python run_pipeline.py --requirements-file examples/sample_requirements.md --project-name demo-project --require-real-llm
```

Offline fallback run:

```bash
python run_pipeline.py --requirements-file examples/sample_requirements.md --project-name demo-project --llm-provider mock --allow-mock
```

The run creates artifacts under `artifacts/<timestamp>_<project>/`:

- `analysis/user_stories.md`
- `development/generated_app/*.py`
- `testing/tests/*.py`
- `reports/test_report.md`
- `reports/bug_summary.md`
- `run_metadata.json`

## Run PM Chatbot UI

```bash
streamlit run app/streamlit_app.py
```

Use the UI to:
- Submit high-level requirements.
- View stage-by-stage progress.
- Track live per-agent activity logs (analysis, design, development, testing).
- Inspect quality outputs and test status.
- Ask PM questions about scope, quality, and completeness even while SDLC is running.

Execution speed controls are available in the sidebar:
- `Fast Mode` to reduce generation overhead.
- `Execute Tests` toggle.
- `Use ChromaDB Embeddings` toggle.
- `Max User Stories` slider.

## CrewAI + LangChain/Hugging Face Modes

- Set `VDP_LLM_PROVIDER=langchain_hf` and add `HUGGINGFACEHUB_API_TOKEN` to use LangChain Hugging Face models.
- Preferred endpoint mode: `VDP_LLM_PROVIDER=langchain_hf_endpoint`
- Optional local transformers mode: `VDP_LLM_PROVIDER=langchain_hf_local`
- Add `VDP_REQUIRE_REAL_LLM=true` to fail fast instead of silently falling back to mock.
- Set `VDP_ENABLE_CREWAI=true` to enable CrewAI handoff planning.
- If dependencies or provider keys are unavailable, the system falls back to deterministic offline behavior.

## Run Tests

```bash
pytest -q
```

## Notes

- Artifacts are intentionally template-driven to simulate enterprise SDLC governance.
- Vector indexing uses ChromaDB when installed and functioning; otherwise a local searchable index is used to keep the workflow operational.
