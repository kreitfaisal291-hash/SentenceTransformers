def chunk_pages(pages: list[dict], chunk_words: int = 120, overlap: int = 30) -> list[dict]:
    """Teilt jede Seite in überlappende Wortblöcke; Metadaten bleiben erhalten."""
    chunks = []
    step = chunk_words - overlap
    for p in pages:
        words = p["text"].split()
        for start in range(0, len(words), step):
            piece = words[start:start + chunk_words]
            if len(piece) < 20:        # winzige Reste überspringen
                continue
            chunks.append({
                "category": p["category"],
                "source": p["source"],
                "page": p["page"],
                "text": " ".join(piece),
            })
    return chunks