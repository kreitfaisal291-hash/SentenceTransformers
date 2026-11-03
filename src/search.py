import re
from typing import Optional

import numpy as np

from src.embedding import get_model, load_index

_index = None


def _get_index():
    global _index
    if _index is None:
        _index = load_index()
    return _index


def _split_passages(text: str, max_words: int = 35) -> list[str]:
    """Zerlegt einen Chunk in Sätze; sehr lange Sätze werden in Blöcke geteilt.
    Jede Passage ist ein exakter Teilstring des Chunks (wichtig fürs Markieren)."""
    passages = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        words = sentence.split()
        if len(words) <= max_words:
            if len(words) >= 4:
                passages.append(sentence)
        else:
            for i in range(0, len(words), max_words):
                part = " ".join(words[i:i + max_words])
                if len(part.split()) >= 4:
                    passages.append(part)
    return passages


def _find_highlights(query_vec: np.ndarray, text: str, n: int = 2, margin: float = 0.08) -> list[str]:
    """Gibt die Passage(n) zurück, die der Anfrage am ähnlichsten sind.
    Eine zweite Passage kommt nur dazu, wenn ihr Score nahe am besten liegt."""
    passages = _split_passages(text)
    if not passages:
        return []
    emb = get_model().encode(passages, normalize_embeddings=True, show_progress_bar=False)
    sims = emb @ query_vec
    order = np.argsort(-sims)
    best = sims[order[0]]
    return [passages[j] for j in order[:n] if sims[j] >= best - margin]


def semantic_search(query: str, category_filter: Optional[str] = None, top_k: int = 5) -> list[dict]:
    """
    1. Suchbegriff in einen Vektor umwandeln
    2. Ähnlichkeit zu allen Chunks berechnen
    3. Nur Chunks der gewünschten Kategorie berücksichtigen
    4. Die besten top_k Treffer samt markierter Stelle zurückgeben und ausdrucken
    category_filter=None oder "all" -> alle Kategorien
    """
    embeddings, chunks = _get_index()

    query_vec = get_model().encode(query, normalize_embeddings=True)
    scores = embeddings @ query_vec

    if category_filter and category_filter.lower() != "all":
        mask = np.array([c["category"].lower() == category_filter.lower() for c in chunks])
        if not mask.any():
            kategorien = sorted({c["category"] for c in chunks})
            raise ValueError(f"Unbekannte Kategorie '{category_filter}'. Verfügbar: {kategorien}")
        scores = np.where(mask, scores, -np.inf)

    best = np.argsort(-scores)[:top_k]

    results = []
    print(f"\nSuche: '{query}'  |  Kategorie: {category_filter or 'all'}  |  Top {top_k}\n")
    for rank, i in enumerate(best, start=1):
        if np.isinf(scores[i]):
            break
        c = chunks[i]
        highlights = _find_highlights(query_vec, c["text"])
        results.append({"score": float(scores[i]), **c, "highlights": highlights})
        print(f"{rank}. [{scores[i]:.3f}] {c['category']} | {c['source']} | Seite {c['page']}")
        print(f"   >> {(highlights[0] if highlights else c['text'][:200])}\n")
    return results