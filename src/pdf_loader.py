from pathlib import Path
from pypdf import PdfReader


def load_pdfs(documents_dir: str = "documents") -> list[dict]:
    """Liest alle PDFs seitenweise ein. Kategorie = Name des Unterordners."""
    pages = []
    root = Path(documents_dir)
    for category_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        for pdf_path in sorted(category_dir.glob("*.pdf")):
            reader = PdfReader(pdf_path)
            for page_no, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({
                        "category": category_dir.name,
                        "source": pdf_path.name,
                        "page": page_no,
                        "text": text,
                    })
    return pages