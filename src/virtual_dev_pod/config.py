from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv(base_dir: Path) -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return

    env_path = base_dir / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)


def _as_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class PodConfig:
    base_dir: Path
    template_dir: Path
    knowledge_dir: Path
    artifact_root: Path
    vector_db_dir: Path
    llm_provider: str
    hf_model_id: str
    hf_api_token: str | None
    require_real_llm: bool
    llm_temperature: float
    llm_max_tokens: int
    enable_crewai: bool
    max_user_stories: int
    top_k_context: int
    fast_mode: bool
    execute_tests: bool
    use_chromadb: bool

    @classmethod
    def from_env(cls, base_dir: Path | None = None) -> "PodConfig":
        root = (base_dir or Path.cwd()).resolve()
        _load_dotenv(root)
        artifact_root = root / os.getenv("VDP_ARTIFACT_DIR", "artifacts")
        vector_db_dir = root / os.getenv("VDP_VECTOR_DB_DIR", "artifacts/vector_db")
        max_user_stories = int(os.getenv("VDP_MAX_USER_STORIES", "5"))
        top_k_context = int(os.getenv("VDP_TOP_K_CONTEXT", "5"))
        fast_mode = _as_bool("VDP_FAST_MODE", False)
        execute_tests = _as_bool("VDP_EXECUTE_TESTS", True)
        use_chromadb = _as_bool("VDP_USE_CHROMADB", not fast_mode)
        llm_temperature = float(os.getenv("VDP_LLM_TEMPERATURE", "0.2"))
        llm_max_tokens = int(os.getenv("VDP_LLM_MAX_TOKENS", "1200"))
        if fast_mode:
            max_user_stories = min(max_user_stories, 3)
            llm_max_tokens = min(llm_max_tokens, 700)
        return cls(
            base_dir=root,
            template_dir=root / "org_repository/templates",
            knowledge_dir=root / "org_repository/knowledge",
            artifact_root=artifact_root,
            vector_db_dir=vector_db_dir,
            llm_provider=os.getenv("VDP_LLM_PROVIDER", "langchain_hf_endpoint"),
            hf_model_id=os.getenv(
                "VDP_HF_MODEL_ID", "mistralai/Mistral-7B-Instruct-v0.2"
            ),
            hf_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            require_real_llm=_as_bool("VDP_REQUIRE_REAL_LLM", True),
            llm_temperature=llm_temperature,
            llm_max_tokens=llm_max_tokens,
            enable_crewai=_as_bool("VDP_ENABLE_CREWAI", False),
            max_user_stories=max_user_stories,
            top_k_context=top_k_context,
            fast_mode=fast_mode,
            execute_tests=execute_tests,
            use_chromadb=use_chromadb,
        )
