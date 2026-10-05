from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import Base, engine
from src.routes import auth, comments, photos, ratings, users

# Створення таблиць у базі даних (якщо вони ще не створені)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PhotoShare API",
    description="REST API для обміну світлинами з підтримкою RBAC, коментарів, рейтингів та профілів.",
    version="1.0.0",
)

# Налаштування CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення роутерів
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(photos.router)
app.include_router(comments.router)
app.include_router(ratings.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to PhotoShare REST API!"}