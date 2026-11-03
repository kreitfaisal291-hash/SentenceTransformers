import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
INDEX_DIR = Path("index")

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
        _model.max_seq_length = 256
    return _model


def embed_texts(texts: list[str], batch_size: int = 32) -> np.ndarray:
    return get_model().encode(
        texts, batch_size=batch_size,
        show_progress_bar=True, normalize_embeddings=True,
    )


def save_index(embeddings: np.ndarray, chunks: list[dict]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    np.save(INDEX_DIR / "embeddings.npy", embeddings)
    (INDEX_DIR / "chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False), encoding="utf-8"
    )


def load_index() -> tuple[np.ndarray, list[dict]]:
    embeddings = np.load(INDEX_DIR / "embeddings.npy")
    chunks = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))
    return embeddings, chunks


def index_exists() -> bool:
    return (INDEX_DIR / "embeddings.npy").exists() and (INDEX_DIR / "chunks.json").exists()