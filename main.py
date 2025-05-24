from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# Загружаем переменные окружения из .env файла
# Это нужно сделать до того, как DATABASE_URL будет прочитан
load_dotenv()

# ---- Модели данных SQLModel ----
class ThoughtBase(SQLModel):
    content: str = Field(index=True)

class Thought(ThoughtBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class ThoughtCreate(ThoughtBase): # Схема для создания
    pass

class ThoughtRead(ThoughtBase): # Схема для чтения
    id: int
    created_at: datetime

# ---- Настройка базы данных ----
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Ошибка: Переменная окружения DATABASE_URL не найдена!")
    print("Пожалуйста, создайте файл .env и укажите в нем DATABASE_URL.")
    exit() # Выход, если URL не задан

engine = create_engine(DATABASE_URL, echo=True) # echo=True для логгирования SQL запросов

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# ---- Управление жизненным циклом приложения (стартап/шатдаун) ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    create_db_and_tables()
    print("База данных и таблицы проверены/созданы.")
    yield
    print("Приложение завершает работу...")

app = FastAPI(title="Thought Board API MVP", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---- Зависимость для получения сессии БД ----
def get_session():
    with Session(engine) as session:
        yield session

# ---- API Эндпоинты ----
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Thought Board API MVP!"}

@app.post("/thoughts/", response_model=ThoughtRead)
def create_thought_endpoint(thought_create: ThoughtCreate, session: Session = Depends(get_session)):
    """
    Создать новую мысль.
    """
    db_thought = Thought.model_validate(thought_create) # Преобразуем ThoughtCreate в Thought
    session.add(db_thought)
    session.commit()
    session.refresh(db_thought)
    return db_thought

@app.get("/thoughts/", response_model=List[ThoughtRead])
def read_thoughts_endpoint(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Получить список мыслей.
    """
    statement = select(Thought).offset(skip).limit(limit).order_by(Thought.created_at.desc())
    thoughts = session.exec(statement).all()
    return thoughts