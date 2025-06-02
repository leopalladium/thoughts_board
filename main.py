from fastapi import FastAPI, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from contextlib import asynccontextmanager
from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .auth import create_access_token, verify_password
from . import auth

# Загружаем переменные окружения из .env файла
# Это нужно сделать до того, как DATABASE_URL будет прочитан
load_dotenv()


# ---- Модели данных SQLModel ----

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    is_admin: bool = False

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    # Убираем связь с мыслями отсюда
    # thoughts: List["Thought"] = Relationship(back_populates="owner")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

# Возвращаем модель Thought к простому виду, без владельца
class ThoughtBase(SQLModel):
    content: str = Field(index=True)

class Thought(ThoughtBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    # Убираем owner_id и связь
    # owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # owner: Optional[User] = Relationship(back_populates="thoughts")

class ThoughtCreate(ThoughtBase):
    pass

class ThoughtRead(ThoughtBase):
    id: int
    created_at: datetime
    # Убираем owner_id и отсюда
    # owner_id: Optional[int] = None

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


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Получение JWT токена по имени пользователя и паролю.
    """
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    # Проверяем, что пользователь существует и пароль верен
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем токен
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}