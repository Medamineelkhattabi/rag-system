"""Script CLI pour indexer le corpus sans passer par l'API.

Usage :
    python -m scripts.ingest               # indexe data/corpus
    python -m scripts.ingest chemin/dossier
"""
from __future__ import annotations

import sys
from pathlib import Path

from app.rag import RAGPipeline


def main() -> None:
    corpus_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    pipeline = RAGPipeline()
    count = pipeline.ingest(corpus_dir=corpus_dir, reset=True)
    print(f"[OK] {count} chunks indexes dans {pipeline.store.index_dir}")


if __name__ == "__main__":
    main()
