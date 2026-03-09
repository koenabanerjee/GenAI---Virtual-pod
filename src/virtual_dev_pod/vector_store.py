from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class SearchHit:
    content: str
    metadata: dict[str, Any]
    score: float


class ArtifactVectorStore:
    def __init__(
        self,
        db_dir: Path,
        *,
        collection_name: str = "virtual_dev_pod",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        enable_chromadb: bool = True,
    ):
        self.db_dir = db_dir
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.db_dir / "memory_index.jsonl"
        self._records: list[dict[str, Any]] = self._load_local_records()
        self._collection = None

        if enable_chromadb:
            try:  # pragma: no cover - dependency boundary
                import chromadb
                from chromadb.utils import embedding_functions

                client = chromadb.PersistentClient(path=str(self.db_dir))
                embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=embedding_model
                )
                self._collection = client.get_or_create_collection(
                    name=collection_name, embedding_function=embedding_fn
                )
            except Exception:
                self._collection = None

    def index_text(self, *, doc_id: str, content: str, metadata: dict[str, Any]) -> None:
        safe_metadata = self._sanitize_metadata(metadata)
        record = {"id": doc_id, "content": content, "metadata": safe_metadata}
        self._records.append(record)
        with self.index_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")

        if self._collection is not None:
            try:  # pragma: no cover - dependency boundary
                self._collection.upsert(
                    ids=[doc_id], documents=[content], metadatas=[safe_metadata]
                )
            except Exception:
                pass

    def index_file(self, *, file_path: Path, artifact_type: str, run_id: str) -> None:
        if not file_path.exists():
            return
        content = file_path.read_text(encoding="utf-8")
        doc_id = f"{run_id}:{artifact_type}:{file_path.name}"
        metadata = {
            "run_id": run_id,
            "artifact_type": artifact_type,
            "path": str(file_path),
        }
        self.index_text(doc_id=doc_id, content=content, metadata=metadata)

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchHit]:
        if self._collection is not None:
            try:  # pragma: no cover - dependency boundary
                kwargs: dict[str, Any] = {"query_texts": [query], "n_results": top_k}
                if metadata_filter:
                    kwargs["where"] = metadata_filter
                result = self._collection.query(**kwargs)
                docs = result.get("documents", [[]])[0]
                metadatas = result.get("metadatas", [[]])[0]
                distances = result.get("distances", [[]])[0]
                hits: list[SearchHit] = []
                for idx, doc in enumerate(docs):
                    metadata = metadatas[idx] if idx < len(metadatas) else {}
                    distance = distances[idx] if idx < len(distances) else 1.0
                    score = 1.0 - float(distance)
                    hits.append(SearchHit(content=doc, metadata=metadata, score=score))
                if hits:
                    return hits
            except Exception:
                pass
        return self._naive_search(query, top_k=top_k, metadata_filter=metadata_filter)

    def _naive_search(
        self, query: str, *, top_k: int, metadata_filter: dict[str, Any] | None = None
    ) -> list[SearchHit]:
        query_tokens = set(_tokenize(query))
        scored: list[SearchHit] = []
        for record in self._records:
            if metadata_filter and not _matches_filter(
                record.get("metadata", {}), metadata_filter
            ):
                continue
            content_tokens = set(_tokenize(record["content"]))
            overlap = len(query_tokens & content_tokens)
            if overlap == 0:
                continue
            score = overlap / max(len(query_tokens), 1)
            scored.append(
                SearchHit(
                    content=record["content"],
                    metadata=record["metadata"],
                    score=score,
                )
            )
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def _load_local_records(self) -> list[dict[str, Any]]:
        if not self.index_path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(json.loads(stripped))
            except json.JSONDecodeError:
                continue
        return records

    def _sanitize_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        safe: dict[str, Any] = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)):
                safe[key] = value
            else:
                safe[key] = str(value)
        return safe


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def _matches_filter(metadata: dict[str, Any], metadata_filter: dict[str, Any]) -> bool:
    for key, expected in metadata_filter.items():
        if metadata.get(key) != expected:
            return False
    return True
