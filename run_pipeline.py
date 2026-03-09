from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from virtual_dev_pod.workflow import VirtualDevelopmentPod  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the AI-powered Virtual Development Pod SDLC workflow."
    )
    parser.add_argument(
        "--requirements-file",
        type=str,
        default="examples/sample_requirements.md",
        help="Path to a markdown or text file containing business requirements.",
    )
    parser.add_argument(
        "--project-name",
        type=str,
        default="virtual-development-pod-demo",
        help="Project name used for generated run artifacts.",
    )
    parser.add_argument(
        "--requirements-text",
        type=str,
        default="",
        help="Inline business requirements. Overrides --requirements-file if provided.",
    )
    parser.add_argument(
        "--llm-provider",
        type=str,
        default="",
        help="Override LLM provider (e.g., langchain_hf_endpoint, langchain_hf_local, mock).",
    )
    parser.add_argument(
        "--require-real-llm",
        action="store_true",
        help="Fail fast if the system cannot initialize a real LLM.",
    )
    parser.add_argument(
        "--allow-mock",
        action="store_true",
        help="Allow mock fallback if real LLM initialization fails.",
    )
    parser.add_argument(
        "--fast-mode",
        action="store_true",
        help="Enable fast mode (fewer heavy steps, lower token budget).",
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test execution to reduce runtime.",
    )
    parser.add_argument(
        "--disable-chromadb",
        action="store_true",
        help="Disable ChromaDB embedding backend and use local fallback search.",
    )
    args = parser.parse_args()

    if args.llm_provider.strip():
        os.environ["VDP_LLM_PROVIDER"] = args.llm_provider.strip()
    if args.allow_mock:
        os.environ["VDP_REQUIRE_REAL_LLM"] = "false"
    if args.require_real_llm:
        os.environ["VDP_REQUIRE_REAL_LLM"] = "true"
    if args.fast_mode:
        os.environ["VDP_FAST_MODE"] = "true"
    if args.skip_tests:
        os.environ["VDP_EXECUTE_TESTS"] = "false"
    if args.disable_chromadb:
        os.environ["VDP_USE_CHROMADB"] = "false"

    if args.requirements_text.strip():
        requirements = args.requirements_text.strip()
    else:
        requirements_path = Path(args.requirements_file)
        if not requirements_path.exists():
            raise FileNotFoundError(f"Requirements file not found: {requirements_path}")
        requirements = requirements_path.read_text(encoding="utf-8")

    try:
        pod = VirtualDevelopmentPod()
        result = pod.run_sdlc(requirements, project_name=args.project_name)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
