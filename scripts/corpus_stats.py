"""Affiche le nombre de documents et de chunks par source dans l'index."""
import json
from collections import Counter

from app.config import settings


def main() -> None:
    meta_path = settings.index_dir / "metadata.json"
    records = json.loads(meta_path.read_text(encoding="utf-8"))
    counts = Counter(r["source"] for r in records)
    print(f"Documents indexes : {len(counts)}")
    print(f"Chunks totaux     : {len(records)}\n")
    print("Chunks par document :")
    for source, n in sorted(counts.items()):
        print(f"  - {source:35s} {n}")


if __name__ == "__main__":
    main()
