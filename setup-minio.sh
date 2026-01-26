#!/bin/bash

# Script para configurar MinIO con Docker para el proyecto de Gestión Integral de Pólizas y Siniestros
# Este script configura el bucket expedientes-siniestros y lo hace público

echo "🚀 Iniciando configuración de MinIO..."

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop primero."
    exit 1
fi

# Verificar si docker-compose.yml existe
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: No se encuentra docker-compose.yml en el directorio actual."
    exit 1
fi

echo "📦 Levantando servicios con Docker Compose..."
docker-compose up -d db minio

# Esperar a que MinIO esté listo
echo "⏳ Esperando a que MinIO esté listo..."
sleep 10

# Verificar que el contenedor MinIO esté corriendo
if ! docker-compose ps minio | grep -q "Up"; then
    echo "❌ Error: El contenedor MinIO no pudo iniciarse correctamente."
    docker-compose logs minio
    exit 1
fi

echo "🔧 Configurando cliente MinIO..."
# Configurar el cliente MinIO dentro del contenedor
docker-compose exec minio mc alias set local http://localhost:9000 admin password123

echo "📁 Creando bucket expedientes-siniestros..."
# Crear el bucket si no existe
docker-compose exec minio mc mb local/expedientes-siniestros --ignore-existing

echo "🌐 Configurando bucket como público..."
# Establecer política de lectura pública
docker-compose exec minio mc anonymous set public local/expedientes-siniestros

echo "✅ Verificando configuración..."
# Verificar que el bucket existe y es público
docker-compose exec minio mc ls local/

echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Resumen de la configuración:"
echo "   - MinIO API: http://localhost:9000"
echo "   - MinIO Console: http://localhost:9001"
echo "   - Usuario: admin"
echo "   - Contraseña: password123"
echo "   - Bucket: expedientes-siniestros (público)"
echo ""
echo "🔗 Los archivos serán accesibles públicamente en:"
echo "   http://localhost:9000/expedientes-siniestros/nombre-del-archivo"
echo ""
echo "🚀 Para levantar la aplicación completa (incluyendo Django):"
echo "   docker-compose up -d"
echo ""
echo "🗄️ Para ejecutar las migraciones de Django:"
echo "   docker-compose exec web python manage.py migrate"
