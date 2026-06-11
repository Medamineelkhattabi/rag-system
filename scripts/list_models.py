"""Diagnostic : liste les modèles Gemini accessibles et leurs actions supportées."""
from google import genai

from app.config import settings


def main() -> None:
    client = genai.Client(api_key=settings.require_api_key())
    print("== Modeles accessibles ==")
    for m in client.models.list():
        actions = getattr(m, "supported_actions", None)
        print(f"{m.name} | {actions}")


if __name__ == "__main__":
    main()
