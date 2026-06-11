"""Client de génération : LLM distant compatible OpenAI (Ollama via Cloudflare Access).

Les embeddings restent assurés par Gemini (voir app/gemini_client.py) ; seule la
génération de la réponse finale passe par ce endpoint.
"""
from __future__ import annotations

import re

import requests

from app.config import settings

SYSTEM_PROMPT = (
    "Tu es un assistant documentaire. Tu réponds aux questions de l'utilisateur "
    "UNIQUEMENT à partir du contexte fourni ci-dessous. "
    "Si la réponse ne se trouve pas dans le contexte, dis clairement que "
    "l'information n'est pas disponible dans les documents. "
    "Réponds en français, de façon concise et factuelle, et cite les sources "
    "entre crochets, par exemple [source: nom_du_fichier]."
)

# Certains modèles « reasoning » (ex. qwen3) émettent un bloc <think>…</think> :
# on le retire pour ne garder que la réponse finale.
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def generate_answer(question: str, context: str) -> str:
    """Génère une réponse ancrée dans le contexte récupéré, via le LLM distant."""
    prompt = (
        f"Contexte :\n{context}\n\n"
        f"Question : {question}\n\n"
        "Réponse (en t'appuyant strictement sur le contexte) :"
    )
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "stream": False,
    }
    response = requests.post(
        f"{settings.llm_base_url}/chat/completions",
        headers=settings.llm_headers(),
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return _THINK_RE.sub("", content or "").strip()
