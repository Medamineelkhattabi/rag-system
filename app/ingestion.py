"""Chargement des documents (TXT, MD, PDF, DOCX) et découpage en chunks."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}


@dataclass
class Chunk:
    """Un fragment de texte prêt à être indexé, avec sa provenance."""

    text: str
    source: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


# Extraction du texte selon le type de fichier
def _read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _read_docx(path: Path) -> str:
    import docx

    document = docx.Document(str(path))
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".txt", ".md"}:
        return _read_txt(path)
    if ext == ".pdf":
        return _read_pdf(path)
    if ext == ".docx":
        return _read_docx(path)
    raise ValueError(f"Extension non supportée : {ext}")


# Découpage en chunks
def _normalize(text: str) -> str:
    # Réduit les espaces multiples et les sauts de ligne excessifs.
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Découpe par paragraphes, en regroupant jusqu'à `chunk_size` caractères,
    avec un recouvrement (`overlap`) pour préserver le contexte aux frontières."""
    text = _normalize(text)
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        # Un paragraphe plus long que la taille cible est coupé durement.
        if len(para) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            for i in range(0, len(para), chunk_size - overlap):
                chunks.append(para[i : i + chunk_size])
            continue

        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            chunks.append(current)
            # Reprend la fin du chunk précédent comme recouvrement.
            tail = current[-overlap:] if overlap else ""
            current = f"{tail}\n\n{para}" if tail else para

    if current:
        chunks.append(current)
    return [c.strip() for c in chunks if c.strip()]


def load_corpus(corpus_dir: Path, chunk_size: int, overlap: int) -> list[Chunk]:
    """Parcourt récursivement un dossier et renvoie la liste de tous les chunks."""
    corpus_dir = Path(corpus_dir)
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Dossier corpus introuvable : {corpus_dir}")

    chunks: list[Chunk] = []
    files = sorted(
        p for p in corpus_dir.rglob("*") if p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    for path in files:
        try:
            raw = extract_text(path)
        except Exception as exc:  # noqa: BLE001 - on ignore un fichier illisible
            print(f"[ingestion] Ignoré {path.name} ({exc})")
            continue
        source = str(path.relative_to(corpus_dir))
        for i, piece in enumerate(chunk_text(raw, chunk_size, overlap)):
            chunks.append(Chunk(text=piece, source=source, chunk_index=i))
    return chunks
