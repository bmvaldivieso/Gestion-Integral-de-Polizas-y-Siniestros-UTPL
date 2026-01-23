## Diagrama de Despligue
<img width="1080" height="990" alt="image" src="https://github.com/user-attachments/assets/c3fd6880-91cb-4d79-a5f3-bcf28dadb664" />

El Diagrama de Despliegue UML que muestra cómo está montada la arquitectura física y lógica del sistema. A continuación, se muestra un resumen de cómo están conectado los componentes y el software del sistema en cuanto a despliegue:

## 1. Clientes (Dispositivos)
El sistema permite el acceso desde distintos dispositivos como Web, PC y una Portátil.

En la portátil, se especifica que el entorno de ejecución es Mozilla, el cual se conecta a la lógica del servidor mediante archivos JSON/XML.

## 2. Servidor Web (Web Server)
- **SO:** Corre sobre Windows 11.
- **Servidor:** Utiliza Apache versión 8.12.
- **App:** La lógica está hecha en Python 3.13 con el framework Django 5.1.3, donde reside la "Capa de Negocio (Services)".

## 3. Servidor de Base de Datos (DataBase Server)
- Se conecta al servidor web por el puerto 3306 (TCP/IP).
- También usa Windows 11 y corre MySQL 8.0.31.
- Dentro tiene los scripts SQL y el modelo físico de datos (Tablas).

**Dato curioso:** aparece un nodo de MinIO SERVER conectado a esta parte para el manejo de objetos o archivos.

