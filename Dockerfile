FROM python:3.12-slim

WORKDIR /app

# Встановлюємо системні залежності
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо та встановлюємо Python-залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Відкриваємо порт FastAPI
EXPOSE 8000

# Команда для запуску
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]