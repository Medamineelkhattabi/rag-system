"""API REST FastAPI exposant le pipeline RAG."""
from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.rag import RAGPipeline

app = FastAPI(
    title="RAG API — Assistant documentaire IA",
    description="Interroge un corpus documentaire et génère des réponses sourcées.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def get_pipeline() -> RAGPipeline:
    return RAGPipeline()


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, examples=["Qu'est-ce qu'un système RAG ?"])
    top_k: int | None = Field(None, ge=1, le=20)


class SourceOut(BaseModel):
    source: str
    score: float
    excerpt: str


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceOut]


class IngestResponse(BaseModel):
    indexed_chunks: int
    message: str


@app.get("/health")
def health() -> dict:
    pipeline = get_pipeline()
    return {
        "status": "ok",
        "indexed_chunks": pipeline.store.size,
        "llm_model": settings.llm_model,
        "embed_model": settings.embed_model,
    }


@app.post("/ingest", response_model=IngestResponse)
def ingest() -> IngestResponse:
    """(Ré)indexe le corpus situé dans data/."""
    try:
        count = get_pipeline().ingest(reset=True)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    if count == 0:
        return IngestResponse(indexed_chunks=0, message="Aucun document trouvé dans le corpus.")
    return IngestResponse(indexed_chunks=count, message=f"{count} chunks indexés.")


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    try:
        result = get_pipeline().query(req.question, top_k=req.top_k)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    sources = [
        SourceOut(
            source=s.source,
            score=round(s.score, 4),
            excerpt=s.text[:300] + ("…" if len(s.text) > 300 else ""),
        )
        for s in result.sources
    ]
    return AskResponse(answer=result.answer, sources=sources)
