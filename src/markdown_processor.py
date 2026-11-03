import re


def clean_text(text: str) -> str:
    text = text.replace("\u00ad", "")          # weiche Trennstriche
    text = re.sub(r"-\n(\w)", r"\1", text)     # Silbentrennung am Zeilenende
    text = re.sub(r"\s*\n\s*", " ", text)      # Zeilenumbrüche -> Leerzeichen
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def process_pages(pages: list[dict], min_chars: int = 50) -> list[dict]:
    for p in pages:
        p["text"] = clean_text(p["text"])
    return [p for p in pages if len(p["text"]) >= min_chars]