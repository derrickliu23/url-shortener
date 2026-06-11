# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# import the engine and Base so we can create tables
from app.database import engine
from app import models

# this creates all tables defined in models.py if they don't exist yet
# safe to run every time — it won't overwrite existing data
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}