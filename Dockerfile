FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip uv


COPY requirements.txt .


RUN python -m uv pip install -r requirements.txt


COPY . .

RUN mkdir -p /app/media

# Exponer puerto
EXPOSE 8000

# Comando de inicio
#CMD ["uvicorn", "todo.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "todo.wsgi:application", "--reload"]
