"""Pipeline RAG : ingestion du corpus, récupération et génération de réponses."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import settings
from app.gemini_client import embed_documents, embed_query
from app.llm_client import generate_answer
from app.ingestion import load_corpus
from app.vectorstore import SearchResult, VectorStore


@dataclass
class RAGAnswer:
    answer: str
    sources: list[SearchResult]


class RAGPipeline:
    def __init__(self, index_dir: Path | None = None):
        self.store = VectorStore(index_dir or settings.index_dir)

    def ingest(self, corpus_dir: Path | None = None, reset: bool = True) -> int:
        """Indexe tous les documents d'un dossier. Renvoie le nombre de chunks."""
        corpus_dir = corpus_dir or settings.corpus_dir
        chunks = load_corpus(corpus_dir, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            return 0

        if reset:
            self.store.reset()

        embeddings = embed_documents([c.text for c in chunks])
        records = [
            {
                "text": c.text,
                "source": c.source,
                "metadata": {"chunk_index": c.chunk_index},
            }
            for c in chunks
        ]
        self.store.add(embeddings, records)
        return len(chunks)

    def query(self, question: str, top_k: int | None = None) -> RAGAnswer:
        question = (question or "").strip()
        if not question:
            return RAGAnswer(answer="Veuillez poser une question.", sources=[])
        if self.store.size == 0:
            return RAGAnswer(
                answer="Aucun document n'est indexé. Lancez d'abord l'ingestion du corpus.",
                sources=[],
            )

        top_k = top_k or settings.top_k
        results = self.store.search(embed_query(question), top_k)

        context = "\n\n---\n\n".join(
            f"[source: {r.source}]\n{r.text}" for r in results
        )
        answer = generate_answer(question, context)
        return RAGAnswer(answer=answer, sources=results)
