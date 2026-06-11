"""Store vectoriel local basé sur NumPy (recherche par similarité cosinus).

Léger et sans dépendance lourde. La même interface `add` / `search` permet de
le remplacer par Chroma, FAISS ou pgvector si besoin de passer à l'échelle.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class SearchResult:
    text: str
    source: str
    score: float
    metadata: dict


class VectorStore:
    def __init__(self, index_dir: Path):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self._vectors_path = self.index_dir / "vectors.npy"
        self._meta_path = self.index_dir / "metadata.json"
        self._vectors: np.ndarray | None = None
        self._records: list[dict] = []
        self._load()

    @staticmethod
    def _normalize(matrix: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return matrix / norms

    def _load(self) -> None:
        if self._vectors_path.exists() and self._meta_path.exists():
            self._vectors = np.load(self._vectors_path)
            self._records = json.loads(self._meta_path.read_text(encoding="utf-8"))

    def _persist(self) -> None:
        if self._vectors is not None:
            np.save(self._vectors_path, self._vectors)
        self._meta_path.write_text(
            json.dumps(self._records, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @property
    def size(self) -> int:
        return len(self._records)

    def reset(self) -> None:
        self._vectors = None
        self._records = []
        if self._vectors_path.exists():
            self._vectors_path.unlink()
        if self._meta_path.exists():
            self._meta_path.unlink()

    def add(self, embeddings: list[list[float]], records: list[dict]) -> None:
        """Ajoute des vecteurs et leurs métadonnées, puis persiste sur disque."""
        if not embeddings:
            return
        new = self._normalize(np.asarray(embeddings, dtype=np.float32))
        self._vectors = new if self._vectors is None else np.vstack([self._vectors, new])
        self._records.extend(records)
        self._persist()

    def search(self, query_embedding: list[float], top_k: int) -> list[SearchResult]:
        if self._vectors is None or self.size == 0:
            return []
        query = np.asarray(query_embedding, dtype=np.float32)
        query /= np.linalg.norm(query) or 1.0
        scores = self._vectors @ query  # cosinus (vecteurs déjà normalisés)
        top_idx = np.argsort(scores)[::-1][:top_k]
        results: list[SearchResult] = []
        for i in top_idx:
            rec = self._records[int(i)]
            results.append(
                SearchResult(
                    text=rec["text"],
                    source=rec["source"],
                    score=float(scores[i]),
                    metadata=rec.get("metadata", {}),
                )
            )
        return results
