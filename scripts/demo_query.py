"""Démonstration : pose une série de questions au pipeline RAG.

Couvre les thèmes du corpus IA + des questions hors corpus (anti-hallucination).
Usage :
    python -m scripts.demo_query        # toutes les questions
    python -m scripts.demo_query 3      # uniquement la question d'indice 3
"""
import sys

from app.rag import RAGPipeline

QUESTIONS = [
    # --- Questions dans le corpus ---
    "Quelle est la différence entre IA, machine learning et deep learning ?",
    "Qu'est-ce qu'un système RAG ?",
    "Pourquoi utilise-t-on des embeddings ?",
    "Quelle est la différence entre RAG et fine-tuning ?",
    "Pourquoi utilise-t-on un overlap entre les chunks ?",
    "Comment fonctionne la similarité cosinus ?",
    "Comment limiter les hallucinations d'un LLM ?",
    "Quels sont les cas d'usage de la vision par ordinateur ?",
    "Qu'est-ce qu'un VLM ?",
    "Quelles sont les bonnes pratiques de prompt engineering ?",
    "Pourquoi ne faut-il jamais exposer une clé API ?",
    "Quelles améliorations seraient nécessaires pour passer en production ?",
    # --- Questions HORS corpus (doivent répondre 'non disponible') ---
    "Quelle est la capitale de l'Australie ?",
    "Quel est le prix actuel du Bitcoin ?",
    "Qui a gagné le dernier match du Real Madrid ?",
    "Quelle est la météo demain à Casablanca ?",
    "Quel est le salaire moyen d'un ingénieur IA au Maroc ?",
]


def main() -> None:
    questions = QUESTIONS
    if len(sys.argv) > 1:
        questions = [QUESTIONS[int(sys.argv[1])]]

    rag = RAGPipeline()
    for q in questions:
        print("=" * 72)
        print(f"Q: {q}")
        result = rag.query(q)
        print(f"\nR: {result.answer}\n")
        print("Sources:")
        for s in result.sources:
            print(f"  - {s.source} (score={s.score:.3f})")
        print()


if __name__ == "__main__":
    main()
