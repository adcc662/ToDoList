FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar herramientas de Python
RUN pip install --upgrade pip uv

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias usando uv
RUN python -m uv pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "todo.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
