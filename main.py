from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
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

# НОВАЯ МОДЕЛЬ USER
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_admin: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    # Связь: один пользователь может иметь много мыслей
    thoughts: List["Thought"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int


# ОБНОВЛЕННАЯ МОДЕЛЬ THOUGHT
class ThoughtBase(SQLModel):
    content: str = Field(index=True)


class Thought(ThoughtBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Связь: каждая мысль принадлежит одному пользователю
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="thoughts")


class ThoughtCreate(ThoughtBase):
    pass


# Добавим связь в схему для чтения
class ThoughtRead(ThoughtBase):
    id: int
    created_at: datetime
    owner_id: Optional[int] = None  # Теперь мы можем видеть, кто автор мысли

# ---- Настройка базы данных ----

# Читаем отдельные компоненты URL из переменных окружения
# Если их нет в .env, можно задать значения по умолчанию
DB_USER = os.getenv("POSTGRES_USER", "leopalladium")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("POSTGRES_DB", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "thoughts_db")
# Конфигурация для вывода SQL запросов (по умолчанию False для продакшена)
DB_ECHO_SQL = os.getenv("DB_ECHO_SQL", "False").lower() == "true"

# Конструируем DATABASE_URL самостоятельно
if not DB_PASSWORD:
    print("Ошибка: Переменная окружения DB_PASSWORD не найдена!")
    print("Проверьте, что переменная DB_PASSWORD определена в .env и передаётся в контейнер через docker-compose.yml.")
    exit() # Выход, если пароль не задан

# Формируем строку подключения
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Используемый DATABASE_URL (без пароля): postgresql+psycopg2://{DB_USER}:*****@{DB_HOST}:{DB_PORT}/{DB_NAME}")
print(f"SQLAlchemy echo (DB_ECHO_SQL): {DB_ECHO_SQL}")

engine = create_engine(DATABASE_URL, echo=DB_ECHO_SQL) # echo=True для логгирования SQL запросов

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

# ---- CORS Middleware ----
origins = [
    "https://klimentsi.live",      # Ваш домен фронтенда
    "https://api.klimentsi.live", # Ваш домен бэкенда
    "http://localhost",           # Для локальной разработки
    "http://localhost:8080",      # Для локальной разработки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
