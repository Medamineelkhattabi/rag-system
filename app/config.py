"""Configuration centralisée, chargée depuis les variables d'environnement (.env)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Charge le fichier .env situé à la racine du projet, s'il existe.
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    # --- Embeddings : Gemini (Google AI Studio) ---
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    embed_model: str = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")

    # --- Génération : LLM distant compatible OpenAI (Ollama derrière Cloudflare Access) ---
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    llm_model: str = os.getenv("LLM_MODEL", "gemma3:12b")
    llm_api_key: str = os.getenv("LLM_API_KEY", "ollama")  # jeton bearer (souvent factice côté Ollama)
    cf_access_client_id: str = os.getenv("CF_ACCESS_CLIENT_ID", "")
    cf_access_client_secret: str = os.getenv("CF_ACCESS_CLIENT_SECRET", "")

    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "150"))
    top_k: int = int(os.getenv("TOP_K", "4"))

    index_dir: Path = ROOT_DIR / os.getenv("INDEX_DIR", "storage")
    corpus_dir: Path = ROOT_DIR / "data"
    api_url: str = os.getenv("API_URL", "http://localhost:8000")

    def require_api_key(self) -> str:
        if not self.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY manquante. Copiez .env.example en .env et renseignez votre clé "
                "(https://aistudio.google.com/app/apikey)."
            )
        return self.gemini_api_key

    def llm_headers(self) -> dict:
        """En-têtes HTTP pour le endpoint de génération (auth Cloudflare Access + bearer)."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.llm_api_key}",
        }
        if self.cf_access_client_id and self.cf_access_client_secret:
            headers["CF-Access-Client-Id"] = self.cf_access_client_id
            headers["CF-Access-Client-Secret"] = self.cf_access_client_secret
        return headers


settings = Settings()
