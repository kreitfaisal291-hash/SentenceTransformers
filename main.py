import sys

from src.pdf_loader import load_pdfs
from src.markdown_processor import process_pages
from src.chunker import chunk_pages
from src.embedding import embed_texts, save_index, index_exists
from src.search import semantic_search


def build_index() -> None:
    pages = process_pages(load_pdfs("documents"))
    chunks = chunk_pages(pages)
    print(f"{len(pages)} Seiten -> {len(chunks)} Chunks")
    embeddings = embed_texts([c["text"] for c in chunks])
    save_index(embeddings, chunks)


if __name__ == "__main__":
    if "--rebuild" in sys.argv or not index_exists():
        build_index()

    kategorien = ["AI", "QuantFinance", "SoftwareArchitecture", "all"]
    while True:
        frage = input("\nFrage (leer = Ende): ").strip()
        if not frage:
            break
        kat = input(f"Kategorie {kategorien}: ").strip() or "all"
        try:
            semantic_search(frage, kat, top_k=5)
        except ValueError as e:
            print(e)