# RAG System

This project is a simple RAG prototype that lets you query a local document corpus
and generate answers based on the provided documents.

The goal is to show a complete RAG pipeline end to end: document ingestion, chunking,
embedding generation, semantic search, context building, and answer generation with
sources.

The project includes a FastAPI backend, a Streamlit interface, and a small demo
document corpus about artificial intelligence.

## How it works

The pipeline runs in two phases.

During ingestion, the documents in the `data/` folder are read, split into chunks
with a small overlap, converted into vectors (embeddings), and stored in a local index.

At query time, the question is also converted into a vector. It is compared to the
indexed vectors using cosine similarity to retrieve the closest passages. These
passages become the context for the language model, which writes an answer based only
on them and cites its sources. If the information is not in the context, the system
says so instead of making up an answer.

## Tech stack

- Python 3.12
- FastAPI for the API
- Streamlit for the interface
- NumPy for the vector index (cosine similarity)
- Gemini for the embeddings
- A generation model exposed through an OpenAI-compatible API (for example Ollama)
- pypdf and python-docx to read PDF and DOCX, reportlab to generate the demo PDF

## Project structure

```
app/         FastAPI API, RAG pipeline, embedding and generation clients, index
frontend/    Streamlit interface
scripts/     ingestion, demo corpus generation, statistics
data/        demo corpus (Markdown, TXT, PDF, DOCX)
storage/     persistent vector index (generated, not versioned)
```

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your values.

```powershell
copy .env.example .env
```

Embeddings use a Gemini API key (free via Google AI Studio). Generation goes through an
OpenAI-compatible API: set its URL and the model name. If the endpoint is protected by
Cloudflare Access, fill in the two headers provided in `.env.example`; otherwise leave
them empty.

No sensitive value should ever be committed: `.env` is ignored by Git.

## Corpus ingestion

```powershell
python -m scripts.build_corpus_assets   # generate the demo PDF and DOCX
python -m scripts.ingest                # index the data/ folder
python -m scripts.corpus_stats          # show the number of documents and chunks
```

Ingestion is also available through the API (`POST /ingest`) or the dedicated button in
the interface.

## Running the backend

```powershell
uvicorn app.api:app --reload --port 8000
```

Interactive documentation is available at http://localhost:8000/docs

## Running the frontend

In a second terminal:

```powershell
streamlit run frontend/streamlit_app.py
```

The interface opens at http://localhost:8501

## Example questions

Questions covered by the corpus:

```
What is a RAG system?
Why do we use embeddings?
How can you limit hallucinations from an LLM?
What are the use cases of computer vision?
```

Out-of-corpus question (the system should answer that the information is not available):

```
What is the capital of Australia?
```

## API endpoints

- `GET /health`: service status, models in use, and number of indexed chunks.
- `POST /ingest`: (re)indexes the corpus in the `data/` folder.
- `POST /ask`: takes a question (`{"question": "..."}`) and returns the answer with its
  sources and their scores.

## Prototype limitations

- The vector index is held in memory and suits a small corpus, not millions of documents.
- Chunking is character-based; sentence-based splitting would be finer.
- There is no re-ranking of the retrieved passages.
- Answer quality depends on the embedding model and the generation model.

## Possible improvements

- Replace the NumPy index with a dedicated vector database to scale up.
- Add re-ranking to improve passage relevance.
- Set up a question/answer test set to evaluate the system.
- Add authentication, access control, and logging.
- Support multiple languages and hybrid (lexical and semantic) search.
