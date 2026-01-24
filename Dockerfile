# Imagen base
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Dependencias del sistema (MySQL + Cairo para PDFs)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libcairo2 \
    libcairo2-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (mejor cache)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
