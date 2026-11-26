from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from core.database import engine, Base, get_db
from core.limiter import limiter
from core.security import get_current_user
from models import user, note, category  # noqa: F401  (регистрация всех моделей в Base)
from models.category import Category
from models.user import User
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from routers import auth, users, notes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сервис заметок")

# Rate Limiting setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
import os as _os

_cors_origins = [o.strip() for o in _os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def read_root():
    return {"message": "Привет, FastAPI! Сервис заметок работает."}


# ---------- Категории (минимальный CRUD, нужен для создания заметок) ----------
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


@app.post("/categories/", response_model=CategoryResponse, tags=["categories"])
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(status_code=400, detail="Категория уже существует")
    category = Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/categories/", response_model=list[CategoryResponse], tags=["categories"])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()