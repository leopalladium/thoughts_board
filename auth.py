from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

# --- НАСТРОЙКИ JWT ---
# Секретный ключ для подписи токенов. В реальном проекте его нужно вынести в .env!
SECRET_KEY = "your-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создаем OAuth2 схему
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- КОНТЕКСТ ДЛЯ ПАРОЛЕЙ (уже был) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- ФУНКЦИИ ДЛЯ ПАРОЛЕЙ (уже были) ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- НОВЫЕ ФУНКЦИИ ДЛЯ JWT ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Создает новый токен доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt