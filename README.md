# URL Shortener

A minimal URL shortener built with FastAPI and SQLite. Paste a long URL, get a short one back, and share it — visiting the short URL redirects to the original.

## How it works

1. User pastes a long URL into the UI and clicks Shorten
2. The frontend sends a POST request to the FastAPI backend
3. The backend generates a random 6-character code and saves it to SQLite alongside the original URL
4. Visiting the short URL triggers a redirect to the original

## Setup

**1. Clone the repo**
```bash
git clone git@github.com:your-username/url-shortener.git
cd url-shortener
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn app.main:app --reload
```

Opens at `http://localhost:8000`.

## Usage

**Via the UI**

Visit `http://localhost:8000`, paste a URL, and hit Shorten. Copy the short URL and share it — visiting it redirects to the original.

**Via the API**

FastAPI generates interactive API docs automatically at `http://localhost:8000/docs`.

Shorten a URL:
```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

Response:
```json
{
  "short_code": "aB3xZ9",
  "short_url": "http://localhost:8000/aB3xZ9",
  "original_url": "https://www.example.com/very/long/url"
}
```

Redirect:
```
GET http://localhost:8000/aB3xZ9 → 307 redirect to original URL
```

## Project structure

```
url-shortener/
├── app/
│   ├── main.py         # FastAPI app, routes, and request/response models
│   ├── database.py     # SQLite connection and session management
│   ├── models.py       # URL table definition
│   └── shortener.py    # short code generation and URL creation logic
├── static/
│   └── index.html      # frontend UI — plain HTML, CSS, and JS
├── venv/
└── requirements.txt
```

## Stack

- [FastAPI](https://fastapi.tiangolo.com) — backend framework
- [SQLite](https://www.sqlite.org) — database (no setup needed, just a file)
- [SQLAlchemy](https://www.sqlalchemy.org) — ORM for database interaction
- [Uvicorn](https://www.uvicorn.org) — ASGI server
- Plain HTML/CSS/JS — frontend (no frameworks)