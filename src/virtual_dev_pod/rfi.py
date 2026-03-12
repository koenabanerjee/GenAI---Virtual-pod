from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Tuple


def extract_text_from_file(file_path: Path) -> str:
    """Read a text-based RFI file and return its plain-text contents.

    Supports .txt and .md directly, and uses :mod:`PyPDF2` for PDF documents.
    """
    ext = file_path.suffix.lower()
    if ext in (".txt", ".md"):
        return file_path.read_text(encoding="utf-8")
    if ext == ".pdf":
        try:
            import PyPDF2
        except ImportError as exc:  # pragma: no cover - needs installer
            raise RuntimeError(
                "PDF support requires PyPDF2; install with `pip install PyPDF2`"
            ) from exc

        text_chunks: list[str] = []
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
        return "\n".join(text_chunks)
    raise ValueError(f"Unsupported RFI file type: {ext}")


def parse_rfi_text(raw_text: str, strict: bool = True) -> Tuple[str, Dict[str, str]]:
    """Convert a block of RFI text into normalized requirement text.

    The RFI is expected to consist of simple ``Field: value`` lines.  At a
    minimum the parser enforces that ``Project Name`` and ``Description`` are
    provided; additional fields are appended to the generated requirement text.

    If strict=False and structured fields are not found, uses a fallback:
    splits the text into project name (first line) and description (rest).

    Returns a tuple ``(requirements_text, fields_dict)``.  ``requirements_text``
    is the plain-text string that can be submitted to the existing pipeline.
    """
    # split on lines and then on the first colon; this is more predictable
    # than trying to rely on multiline regex (which was behaving
    # inconsistently on Windows during testing).
    fields: Dict[str, str] = {}
    for line in raw_text.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if key:
            fields[key] = val

    required = ["Project Name", "Description"]
    missing = [f for f in required if not fields.get(f)]
    
    if missing:
        if strict:
            raise ValueError(f"RFI missing required fields: {', '.join(missing)}")
        # fallback: use heuristics to extract project name and description
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        if not lines:
            raise ValueError("Uploaded document is empty.")
        # first line becomes project name, rest becomes description
        fields["Project Name"] = lines[0][:100]  # limit to 100 chars
        fields["Description"] = "\n".join(lines[1:]) if len(lines) > 1 else lines[0]

    # build output text; start with a header so the pipeline still sees something
    parts: list[str] = []
    parts.append(f"# {fields.get('Project Name')}")
    parts.append(fields.get("Description", ""))

    # append any leftover fields
    for key in fields:
        if key not in required:
            parts.append(f"**{key}**: {fields[key]}")

    return "\n\n".join(parts).strip(), fields


def load_rfi(path: Path, strict: bool = True) -> str:
    """High‑level helper: read an RFI file and return requirements text.

    This pulls the raw text from ``path`` and then runs
    :func:`parse_rfi_text`.  
    
    If strict=True (default), raises ValueError for unsupported file extensions
    or when required fields are missing.
    If strict=False, uses fallback heuristics to extract project name and
    description when structured fields are not found (useful for PDFs).
    """
    raw = extract_text_from_file(path)
    try:
        requirements, _ = parse_rfi_text(raw, strict=strict)
    except ValueError as exc:
        # automatically fall back to lenient parsing if required-fields are missing
        msg = str(exc)
        if strict and "missing required fields" in msg:
            requirements, _ = parse_rfi_text(raw, strict=False)
        else:
            raise
    return requirements
