from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from src.embedding import get_model, index_exists
from src.search import _get_index, semantic_search

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Modell und Index einmal beim Start laden, nicht bei jeder Anfrage
    if not index_exists():
        raise RuntimeError("Kein Index gefunden. Erst 'python main.py --rebuild' ausführen.")
    get_model()
    _get_index()
    yield


app = FastAPI(title="Semantische Dokumentensuche", lifespan=lifespan)


@app.get("/api/categories")
def categories():
    _, chunks = _get_index()
    return sorted({c["category"] for c in chunks})


@app.get("/api/search")
def search(
    q: str = Query(..., min_length=2),
    category: str = "all",
    top_k: int = Query(3, ge=1, le=10),
):
    try:
        return semantic_search(q, category, top_k=top_k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")