# Simple Social Media

A lightweight full-stack social media app where users can upload images and videos, browse a live feed, and delete posts — all backed by a FastAPI REST API and ImageKit CDN storage.

---

## ✨ Features

- 📤 Upload images and videos with captions
- 🖼️ Browse a chronological media feed
- 🗑️ Delete posts by UUID
- ☁️ Media stored and served via ImageKit CDN
- ⚡ Async backend with SQLAlchemy + SQLite

---

## 🛠️ Tech Stack

| Layers        | Technology                          |
|---------------|-------------------------------------|
| Backend       | FastAPI, SQLAlchemy (Async), Uvicorn |
| Database      | SQLite via `aiosqlite`              |
| Frontend      | Streamlit                           |
| Media Storage | ImageKit CDN                        |

---

## 📁 Project Structure

```
Simple-social-media/
│
├── src/
│   ├── app.py          # FastAPI routes
│   ├── db.py           # Database models & session
│   ├── image.py        # ImageKit client setup
│   ├── schema.py       # Pydantic schemas
│   └── frontend.py     # Streamlit UI
│
├── .env                # Environment variables
├── pyproject.toml
└── README.md
```

---

## 🚀 Running the App

### Start the backend

```bash
uvicorn src.app:app --reload
```

API available at → `http://127.0.0.1:8000`  
Interactive docs at → `http://127.0.0.1:8000/docs`

### Start the frontend

```bash
streamlit run src/frontend.py
```

UI available at → `http://localhost:8501`

---

## 🗺️ Example Workflow

1. Run the FastAPI backend
2. Run the Streamlit frontend
3. Upload an image or video with a caption
4. View it appear in the feed instantly
5. Delete any post with one click
