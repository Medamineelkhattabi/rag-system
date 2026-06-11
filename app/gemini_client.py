"""Encapsulation du SDK Gemini : embeddings du corpus et des requêtes.

La génération des réponses est assurée par un LLM distant (voir app/llm_client.py).
"""
from __future__ import annotations

from functools import lru_cache

from google import genai
from google.genai import types

from app.config import settings


@lru_cache(maxsize=1)
def _client() -> genai.Client:
    return genai.Client(api_key=settings.require_api_key())


def _embed(texts: list[str], task_type: str) -> list[list[float]]:
    # task_type : RETRIEVAL_DOCUMENT pour l'indexation, RETRIEVAL_QUERY pour les requêtes.
    client = _client()
    vectors: list[list[float]] = []
    batch_size = 100
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = client.models.embed_content(
            model=settings.embed_model,
            contents=batch,
            config=types.EmbedContentConfig(task_type=task_type),
        )
        vectors.extend(emb.values for emb in response.embeddings)
    return vectors


def embed_documents(texts: list[str]) -> list[list[float]]:
    return _embed(texts, task_type="RETRIEVAL_DOCUMENT")


def embed_query(text: str) -> list[float]:
    return _embed([text], task_type="RETRIEVAL_QUERY")[0]
