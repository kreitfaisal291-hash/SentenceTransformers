from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pdf_loader import load_pdfs
from src.markdown_processor import process_pages
from src.chunker import chunk_pages
from src.embedding import embed_texts, save_index, index_exists
from src.search import semantic_search

app = FastAPI()  # <--- Das ist die Instanz, die die Plattform sucht!

# Index beim Start aufbauen, falls nicht vorhanden
@app.on_event("startup")
def startup_event():
    if not index_exists():
        pages = process_pages(load_pdfs("documents"))
        chunks = chunk_pages(pages)
        embeddings = embed_texts([c["text"] for c in chunks])
        save_index(embeddings, chunks)

class QueryRequest(BaseModel):
    frage: str
    kategorie: str = "all"

@app.post("/search")
def search_endpoint(request: QueryRequest):
    try:
        # Hier müsstest du deine semantic_search anpassen, 
        # damit sie die Ergebnisse als JSON zurückgibt statt nur zu printen
        ergebnisse = semantic_search(request.frage, request.kategorie, top_k=5)
        return {"ergebnisse": ergebnisse}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))