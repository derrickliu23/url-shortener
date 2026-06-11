# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles

# RedirectResponse sends the user to a different URL
# For getting the link
from fastapi.responses import RedirectResponse, FileResponse

# BaseModel is used to define the shape of request/response data
from pydantic import BaseModel

from app.database import engine, get_db
from app import models
from app.shortener import create_short_url
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- request body shape ---
# when the frontend sends a POST request to /shorten,
# FastAPI expects the body to look like: { "url": "https://..." }
class ShortenRequest(BaseModel):
    url: str

# --- shorten route ---
# POST /shorten accepts a long URL and returns a short code
@app.post("/shorten")
def shorten_url(request: ShortenRequest, db: Session = Depends(get_db)):
    # Depends(get_db) tells FastAPI to call get_db() and pass the
    # session in as `db` — it handles opening and closing automatically

    code = create_short_url(request.url, db)

    # return the full short URL so the frontend can display it
    return {
        "short_code": code,
        "short_url": f"http://localhost:8000/{code}",
        "original_url": request.url
    }

# --- redirect route ---
# GET /{code} looks up the short code and redirects to the original URL
@app.get("/{code}")
def redirect_url(code: str, db: Session = Depends(get_db)):
    # look up the short code in the database
    url = db.query(models.URL).filter(models.URL.short_code == code).first()

    # if the code doesn't exist, return a 404 error
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # 307 is a temporary redirect — the browser follows it automatically
    return RedirectResponse(url=url.original_url, status_code=307)

@app.get("/health")
def health():
    return {"status": "ok"}

# serve the HTML UI at the root URL
@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")