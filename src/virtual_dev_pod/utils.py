from __future__ import annotations

import json
import re
from datetime import datetime, timezone


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "generated_item"


def safe_class_name(text: str) -> str:
    parts = [piece for piece in slugify(text).split("_") if piece]
    if not parts:
        return "GeneratedService"
    return "".join(p.capitalize() for p in parts) + "Service"


def trim_words(text: str, max_words: int = 30) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).strip() + "..."


def extract_json_payload(text: str) -> dict | list | None:
    if not text:
        return None

    fenced = re.findall(r"```json\s*(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    for block in fenced:
        payload = _load_json_safely(block)
        if payload is not None:
            return payload

    fenced_any = re.findall(r"```\s*(.*?)```", text, flags=re.DOTALL)
    for block in fenced_any:
        payload = _load_json_safely(block)
        if payload is not None:
            return payload

    payload = _load_json_safely(text)
    if payload is not None:
        return payload

    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch not in "[{":
            continue
        try:
            obj, _ = decoder.raw_decode(text[i:])
            return obj
        except json.JSONDecodeError:
            continue
    return None


def _load_json_safely(content: str) -> dict | list | None:
    cleaned = content.strip()
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None
