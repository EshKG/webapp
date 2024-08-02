# Используем базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /bot

# Копируем файл зависимостей
COPY bot/ ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код бота
COPY . /bot

# Запускаем бота
CMD ["python", "main.py"]
