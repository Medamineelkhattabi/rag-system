"""Interface chat Streamlit pour le système RAG (consomme l'API FastAPI)."""
from __future__ import annotations

import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Assistant documentaire IA (RAG)", page_icon="📄", layout="centered")

st.title("📄 Assistant documentaire (RAG)")
st.caption("Posez vos questions sur le corpus — les réponses sont ancrées dans les documents, avec leurs sources.")

# Barre latérale : état de l'API et (ré)indexation
with st.sidebar:
    st.header("⚙️ Administration")
    st.write(f"**API :** `{API_URL}`")

    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        st.success("API connectée")
        st.metric("Chunks indexés", health.get("indexed_chunks", 0))
        st.write(f"**Modèle LLM :** {health.get('llm_model')}")
        st.write(f"**Modèle embed :** {health.get('embed_model')}")
    except Exception:
        st.error("API injoignable. Lancez le backend FastAPI.")

    if st.button("🔄 (Ré)indexer le corpus", use_container_width=True):
        with st.spinner("Indexation en cours…"):
            try:
                resp = requests.post(f"{API_URL}/ingest", timeout=300).json()
                st.success(resp.get("message", "Terminé."))
            except Exception as exc:  # noqa: BLE001
                st.error(f"Échec : {exc}")

    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(
                        f"**{s['source']}** — score {s['score']}\n\n> {s['excerpt']}"
                    )

if question := st.chat_input("Votre question…"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents…"):
            try:
                resp = requests.post(
                    f"{API_URL}/ask", json={"question": question}, timeout=120
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data["answer"]
                sources = data.get("sources", [])
            except Exception as exc:  # noqa: BLE001
                answer = f"Erreur lors de l'appel à l'API : {exc}"
                sources = []

        st.markdown(answer)
        if sources:
            with st.expander("📚 Sources"):
                for s in sources:
                    st.markdown(f"**{s['source']}** — score {s['score']}\n\n> {s['excerpt']}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )
