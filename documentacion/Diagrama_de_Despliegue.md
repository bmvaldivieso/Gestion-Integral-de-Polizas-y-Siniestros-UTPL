## Diagrama de Despligue
<img width="1963" height="738" alt="image" src="https://github.com/user-attachments/assets/c085ede9-770c-4817-965f-cc61c91db12e" />

## Capa de Almacenamiento – MinIO en Docker

MinIO se ejecuta exclusivamente en **Docker** para simular un almacenamiento compatible con **Amazon S3**.

### Configuración

- **Contenedor:** `minio/minio`  
  - Servidor API: puerto **9000**  
  - Consola web: puerto **9001**  
  - Definido en `docker-compose.yml` (líneas 14–25)

- **Bucket:** `expedientes-siniestros`  
  - Configurado como **público**  
  - Creado y configurado en `setup-minio.sh` (líneas 38–44)

- **Persistencia:**  
  - Volumen Docker `minio_data`  
  - Garantiza almacenamiento persistente de los archivos  
  - Definido en `docker-compose.yml` (líneas 21–22)

## Capa de Aplicación – Django Nativo

La aplicación está desarrollada en **Django** y se ejecuta directamente en el sistema local, sin uso de contenedores.

### Configuración

- **Ejecución:**  
  - Comando: `python manage.py runserver 0.0.0.0:8000`  
  - Servidor accesible desde la red local en el puerto **8000**

- **Configuración MySQL:**  
  - Conexión a una instancia **MySQL local**  
  - Parámetros definidos mediante **variables de entorno**  
  - Configuración ubicada en `settings.py` (líneas 79–91)

- **Modo transaccional:**  
  - MySQL configurado con `STRICT_TRANS_TABLES`  
  - Garantiza integridad y consistencia de los datos  
  - Definido en `settings.py` (líneas 87–89)

## Capa de Datos – MySQL

La base de datos **MySQL** se ejecuta de forma nativa en el sistema o alternativamente en **Docker**, según la configuración del entorno.

### Configuración

- **Motor:**  
  - MySQL **8.0**  
  - Definido según la configuración del pipeline de CI  
  - Referenciado en `ci.yml` (líneas 57–61)

- **Conexión:**  
  - Django se conecta mediante el driver `mysqlclient`  
  - Uso de credenciales locales para el acceso a la base de datos

- **Configuración de la base de datos:**  
  - Nombre de la base de datos: `polizas`  
  - Usuario: `root`  
  - Contraseña configurada mediante variables de entorno
## Configuración de Integración

### Django Settings

El archivo `settings.py` centraliza la configuración de integración entre la **capa de aplicación desarrollada en Django**, el **servicio de almacenamiento MinIO ejecutado en Docker** y la **base de datos MySQL nativa**.

Esta arquitectura permite separar responsabilidades, facilitando la escalabilidad, el mantenimiento y la interoperabilidad entre componentes.

- Archivo de configuración: `settings.py`  
- Líneas relevantes: 149–170

```
# Conexión a MinIO en Docker  
STORAGES = {  
    "default": {  
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",  
        "OPTIONS": {  
            "access_key": "admin",  
            "secret_key": "password123",  
            "bucket_name": "expedientes-siniestros",  
            "endpoint_url": "http://localhost:9000",  
            "use_ssl": False,  
            "verify": False,  
        },  
    },  
}

# Conexión a MySQL nativo  
DATABASES = {  
    "default": {  
        "ENGINE": "django.db.backends.mysql",  
        "NAME": "polizas",  
        "USER": "root",  
        "HOST": "127.0.0.1",  
        "PORT": "3306",  
    }  
}
```
## Flujo de Despliegue

### 1. Configuración de MinIO en Docker
```
# Iniciar solo MinIO  
docker-compose up -d minio  
  
# Configurar bucket  
./setup-minio.sh
```
### 2. Configuración de MySQL Local
```
# Crear base de datos  
mysql -u root -p -e "CREATE DATABASE polizas;"  
  
# Configurar variables de entorno  
export DATABASE_NAME=polizas  
export DATABASE_USER=root  
export DATABASE_PASSWORD=tu_contraseña
```
### 3. Ejecución de Django Nativo
```
# Instalar dependencias  
pip install -r requirements.txt  
  
# Migraciones  
python manage.py migrate  
  
# Iniciar servidor  
python manage.py runserver 0.0.0.0:8000
```
## Ventajas de esta Arquitectura

La arquitectura adoptada ofrece múltiples beneficios tanto para el desarrollo como para el despliegue y mantenimiento del sistema.

### Desarrollo Rápido

- **Hot-reloading:**  
  Los cambios realizados en el código se reflejan inmediatamente en la aplicación, agilizando el ciclo de desarrollo.

- **Debugging eficiente:**  
  Acceso directo a los procesos de Django sin el overhead asociado a la contenerización, facilitando la depuración.

- **Optimización de recursos:**  
  Menor consumo de recursos del sistema al ejecutar Django de forma nativa, especialmente en entornos de desarrollo.

### Aislamiento de Servicios

- **MinIO aislado:**  
  El almacenamiento compatible con S3 se ejecuta en un contenedor independiente, evitando dependencias locales y conflictos de configuración.

- **MySQL dedicado:**  
  La base de datos se mantiene persistente e independiente del código de la aplicación.

- **Portabilidad:**  
  Facilita la migración entre entornos de desarrollo, pruebas y producción con mínimos ajustes.

### Configuración Flexible

- **Uso de variables de entorno:**  
  Permite una adaptación rápida a diferentes configuraciones sin modificar el código fuente.

- **Desacoplamiento de componentes:**  
  Cada servicio puede escalarse o modificarse de manera independiente según las necesidades del sistema.

- **Facilidad de testing:**  
  La separación de responsabilidades simplifica la ejecución de pruebas unitarias y de integración.

