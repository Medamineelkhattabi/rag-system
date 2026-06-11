# RAG System

Ce projet est un prototype simple de système RAG permettant d'interroger un corpus
documentaire local et de générer des réponses basées sur les documents fournis.

L'objectif est de montrer le fonctionnement complet d'un pipeline RAG : ingestion de
documents, découpage en chunks, génération d'embeddings, recherche sémantique,
construction du contexte et génération d'une réponse avec ses sources.

Le projet contient une API FastAPI, une interface Streamlit et un petit corpus
documentaire de démonstration autour de l'intelligence artificielle.

## Fonctionnement général

Le pipeline se déroule en deux temps.

À l'ingestion, les documents du dossier `data/` sont lus, découpés en fragments
(chunks) avec un léger recouvrement, convertis en vecteurs (embeddings) et stockés
dans un index local.

À l'interrogation, la question est elle aussi convertie en vecteur. On compare ce
vecteur à ceux de l'index par similarité cosinus pour récupérer les passages les plus
proches. Ces passages servent de contexte au modèle de langage, qui rédige une réponse
en s'appuyant uniquement sur eux et en citant ses sources. Si l'information ne se
trouve pas dans le contexte, le système l'indique au lieu d'inventer une réponse.

## Technologies utilisées

- Python 3.12
- FastAPI pour l'API
- Streamlit pour l'interface
- NumPy pour l'index vectoriel (similarité cosinus)
- Gemini pour les embeddings
- Un modèle de génération exposé via une API compatible OpenAI (par exemple Ollama)
- pypdf et python-docx pour lire les PDF et DOCX, reportlab pour générer le PDF de démo

## Structure du projet

```
app/         API FastAPI, pipeline RAG, clients embeddings et génération, index
frontend/    interface Streamlit
scripts/     ingestion, génération du corpus de démo, statistiques
data/        corpus de démonstration (Markdown, TXT, PDF, DOCX)
storage/     index vectoriel persistant (généré, non versionné)
```

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Copiez `.env.example` en `.env` et renseignez vos valeurs.

```powershell
copy .env.example .env
```

Les embeddings utilisent une clé Gemini (gratuite via Google AI Studio). La génération
passe par une API compatible OpenAI : indiquez son URL et le nom du modèle. Si
l'endpoint est protégé par Cloudflare Access, renseignez les deux en-têtes prévus dans
`.env.example` ; sinon laissez-les vides.

Aucune valeur sensible ne doit être commitée : `.env` est ignoré par Git.

## Ingestion du corpus

```powershell
python -m scripts.build_corpus_assets   # génère le PDF et le DOCX de démo
python -m scripts.ingest                # indexe le dossier data/
python -m scripts.corpus_stats          # affiche le nombre de documents et de chunks
```

L'ingestion est aussi accessible via l'API (`POST /ingest`) ou le bouton dédié dans
l'interface.

## Lancement du backend

```powershell
uvicorn app.api:app --reload --port 8000
```

La documentation interactive est disponible sur http://localhost:8000/docs

## Lancement du frontend

Dans un second terminal :

```powershell
streamlit run frontend/streamlit_app.py
```

L'interface s'ouvre sur http://localhost:8501

## Exemples de questions

Questions couvertes par le corpus :

```
Qu'est-ce qu'un système RAG ?
Pourquoi utilise-t-on des embeddings ?
Comment limiter les hallucinations d'un LLM ?
Quels sont les cas d'usage de la vision par ordinateur ?
```

Question hors corpus (le système doit répondre que l'information n'est pas disponible) :

```
Quelle est la capitale de l'Australie ?
```

## Endpoints de l'API

- `GET /health` : état du service, modèles utilisés et nombre de chunks indexés.
- `POST /ingest` : (ré)indexe le corpus du dossier `data/`.
- `POST /ask` : prend une question (`{"question": "..."}`) et renvoie la réponse avec
  ses sources et leurs scores.

## Limites du prototype

- L'index vectoriel tient en mémoire et convient à un petit corpus, pas à des millions
  de documents.
- Le découpage se fait par caractères ; un découpage par phrases serait plus fin.
- Il n'y a pas de reclassement (re-ranking) des passages récupérés.
- La qualité des réponses dépend du modèle d'embeddings et du modèle de génération.

## Améliorations possibles

- Remplacer l'index NumPy par une base vectorielle dédiée pour passer à l'échelle.
- Ajouter un re-ranking pour améliorer la pertinence des passages.
- Mettre en place un jeu de questions/réponses pour évaluer le système.
- Ajouter l'authentification, la gestion des accès et la journalisation.
- Gérer le multilingue et une recherche hybride (lexicale et sémantique).
