# generate_db_password.sh (на хосте, рядом с docker-compose.yml)
#!/bin/bash

# Путь к .env файлу на хосте
ENV_FILE="./.env"

# Проверяем, существует ли .env файл, если нет - создаем
if [ ! -f "$ENV_FILE" ]; then
  touch "$ENV_FILE"
fi

# Проверяем, существует ли переменная DB_PASSWORD в .env файле
if grep -q "^DB_PASSWORD=" "$ENV_FILE"; then
  echo "DB_PASSWORD already exists in $ENV_FILE. Skipping generation."
else
  # Генерируем случайный пароль
  GENERATED_PASSWORD=$(head /dev/urandom | tr -dc A-Za-z0-9\$\&\-\_\=\+\!\@\#\%\^\*\(\)\[\]\{\}\;\:\'\"\,\.\<\>\/\?~ | head -c 32 ; echo)

  echo "Generating new DB_PASSWORD and appending to $ENV_FILE"
  echo "DB_PASSWORD=$GENERATED_PASSWORD" >> "$ENV_FILE"
  chmod 600 "$ENV_FILE" # Устанавливаем правильные права для .env
fi

# Если вам нужно, чтобы другие параметры (DB_HOST, DB_USER, DB_NAME)
# также были в .env, можете добавить их сюда, но для данной задачи
# их можно жестко задать в main.py, так как они, вероятно, не меняются.

# Например, если вы хотите, чтобы DB_USER и DB_NAME тоже были в .env:
if ! grep -q "^DB_USER=" "$ENV_FILE"; then echo "DB_USER=leopalladium" >> "$ENV_FILE"; fi
if ! grep -q "^DB_NAME=" "$ENV_FILE"; then echo "DB_NAME=thoughts_db" >> "$ENV_FILE"; fi
if ! grep -q "^DB_HOST=" "$ENV_FILE"; then echo "DB_HOST=db" >> "$ENV_FILE"; fi # Имя сервиса БД
if ! grep -q "^DB_PORT=" "$ENV_FILE"; then echo "DB_PORT=5432" >> "$ENV_FILE"; fi # Порт БД

echo "DB_PASSWORD, DB_USER, DB_NAME, DB_HOST, DB_PORT verified/generated in .env"