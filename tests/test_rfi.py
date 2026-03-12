import os
import shutil
from pathlib import Path

import pytest

from virtual_dev_pod.rfi import extract_text_from_file, load_rfi, parse_rfi_text
from virtual_dev_pod.config import PodConfig
from virtual_dev_pod.workflow import VirtualDevelopmentPod


def test_parse_rfi_text_valid():
    raw = """Project Name: Example Project
Description: Build a demo service
Additional Info: some extra details"""
    requirements, fields = parse_rfi_text(raw)
    assert "Example Project" in requirements
    assert "Build a demo service" in requirements
    assert "Additional Info" in requirements
    assert fields["Project Name"] == "Example Project"


def test_parse_rfi_text_missing_required():
    raw = "Description: only desc, no project name"
    with pytest.raises(ValueError):
        parse_rfi_text(raw, strict=True)


def test_parse_rfi_text_fallback_mode():
    """Test that unstructured text can be parsed with strict=False."""
    raw = """Weather Prediction System
This line is the description about
building a sophisticated weather prediction system."""
    requirements, fields = parse_rfi_text(raw, strict=False)
    assert "Weather Prediction System" in fields["Project Name"]
    assert "This line is the description" in fields["Description"]
    assert "# Weather Prediction System" in requirements


def test_extract_text_from_pdf(tmp_path):
    # create a simple PDF with the fpdf package so PyPDF2 can read it
    try:
        from fpdf import FPDF
    except ImportError:
        pytest.skip("fpdf not installed; skipping PDF extraction test")

    pdf_path = tmp_path / "sample.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Project Name: PDFTest", ln=True)
    pdf.cell(0, 10, "Description: from pdf", ln=True)
    pdf.output(str(pdf_path))

    text = extract_text_from_file(pdf_path)
    assert "PDFTest" in text
    assert "from pdf" in text


def test_workflow_accepts_rfi_and_copies_original(tmp_path):
    # set up a minimal pod configuration using the mock LLM
    root = Path(__file__).resolve().parents[1]
    tmp_root = root / "artifacts" / "_test_tmp_workflow_rfi"
    if tmp_root.exists():
        shutil.rmtree(tmp_root, ignore_errors=True)
    tmp_root.mkdir(parents=True, exist_ok=True)

    config = PodConfig(
        base_dir=root,
        template_dir=root / "org_repository/templates",
        knowledge_dir=root / "org_repository/knowledge",
        artifact_root=tmp_root / "artifacts",
        vector_db_dir=tmp_root / "vector_db",
        llm_provider="mock",
        hf_model_id="mistralai/Mistral-7B-Instruct-v0.2",
        hf_api_token=None,
        require_real_llm=False,
        llm_temperature=0.2,
        llm_max_tokens=800,
        enable_crewai=False,
        max_user_stories=3,
        top_k_context=3,
        fast_mode=False,
        execute_tests=False,
        use_chromadb=False,
    )
    pod = VirtualDevelopmentPod(config=config)

    # write a simple RFI file and run the workflow using the parser helper
    rfi_file = tmp_path / "upload.txt"
    rfi_file.write_text(
        """Project Name: RFI Test\nDescription: this is a requirement from an RFI"""
    )

    requirements = load_rfi(rfi_file)
    result = pod.run_sdlc(requirements, project_name="rfi-project", original_input_path=rfi_file)

    assert "RFI Test" in result.requirements
    # verify copy exists and metadata was updated
    copied = Path(result.original_input) if result.original_input else None
    assert copied is not None and copied.exists()
    assert copied.read_text().startswith("Project Name")


def test_load_rfi_fallback(tmp_path):
    """load_rfi should succeed even when strict=True would complain.

    The helper now automatically retries with strict=False when fields are
    missing, which is important for PDFs whose text extraction may strip
    colons or formatting.
    """
    txt = tmp_path / "simple.txt"
    txt.write_text("Just a project title\nsome description text")
    result = load_rfi(txt)
    assert "Just a project title" in result
    assert result.startswith("# Just a project title")

    # also exercise PDF path where extraction might lose field labels
    try:
        from fpdf import FPDF
    except ImportError:
        # fpdf not installed in this environment; skip PDF portion
        return
    pdf_path = tmp_path / "nofields.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "No structured data here", ln=True)
    pdf.cell(0, 10, "Just a title and description", ln=True)
    pdf.output(str(pdf_path))
    pdf_req = load_rfi(pdf_path)
    assert "# No structured data here" in pdf_req


def test_cli_accepts_rfi(tmp_path, capsys):
    # exercise run_pipeline.py using rfi-file argument
    from run_pipeline import main as cli_main
    from pathlib import Path
    import sys
    
    root = Path(__file__).resolve().parents[1]
    rfi_path = tmp_path / "cli_upload.txt"
    rfi_path.write_text("Project Name: CLI RFI\nDescription: used by CLI test")
    
    # build argv
    # force mock LLM via environment so CLI doesn't try to contact HF
    os.environ["VDP_LLM_PROVIDER"] = "mock"
    os.environ["VDP_REQUIRE_REAL_LLM"] = "false"

    sys_argv = sys.argv
    try:
        sys.argv = ["run_pipeline.py", "--rfi-file", str(rfi_path), "--project-name", "cli-test"]
        cli_main()
        captured = capsys.readouterr()
        # JSON output should include original_input path and project name
        import json
        result = json.loads(captured.out)
        assert result.get("project_name") == "cli-test"
        assert result.get("original_input") is not None
        assert Path(result["original_input"]).exists()
        # UI artifacts should be returned as list
        assert isinstance(result.get("ui_artifacts"), list)
    finally:
        sys.argv = sys_argv
