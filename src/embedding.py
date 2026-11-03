import os
from openai import OpenAI

# Der Client greift automatisch auf die Umgebungsvariable OPENAI_API_KEY zu
client = OpenAI()

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Erstellt Embeddings über die OpenAI API – benötigt kein lokales PyTorch mehr."""
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-small"
    )
    return [item.embedding for item in response.data]

def save_index(embeddings, chunks):
    # WICHTIG bei Vercel: Das Dateisystem ist read-only (außer /tmp).
    # Lokales Speichern von Dateien funktioniert hier im Serverless-Betrieb nicht dauerhaft.
    pass

def index_exists() -> bool:
    return False