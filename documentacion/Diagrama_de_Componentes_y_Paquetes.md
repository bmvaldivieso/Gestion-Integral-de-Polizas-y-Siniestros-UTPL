# Diagramade Componentes
<img width="2265" height="2094" alt="image" src="https://github.com/user-attachments/assets/03f34947-7f8d-4b1e-8fbc-3d7381155c4a" />

# Descripción del Diagrama de Componentes
El sistema implementa una **arquitectura de tres capas estricta** con separación de responsabilidades, construida sobre el framework **Django**.  
Esta estructura garantiza **mantenibilidad, testabilidad y escalabilidad** del código mediante dependencias unidireccionales controladas.

---

## Flujo de Comunicación
El sistema sigue un flujo unidireccional donde las solicitudes HTTP atraviesan las capas en orden:

**Presentación → Negocio → Datos → Persistencia**

Esta separación garantiza que cada capa tenga responsabilidades bien definidas sin violar las dependencias  

---

## Capa de Presentación

### Controladores HTTP (`views.py`)
Las vistas Django manejan solicitudes HTTP y coordinan con la capa de negocio:

- **LoginView**: Maneja autenticación universal con redirección por rol (*views.py:1-55*).
- **DashboardAdminView / DashboardAnalistaView**: Paneles especializados según rol de usuario.
- **PolizaListView**: Gestión CRUD completa de pólizas con validaciones.
- **SiniestroListView**: Procesamiento del ciclo de vida de siniestros.
- **FiniquitoCreateView**: Liquidación final con cálculos automáticos.

Cada vista implementa control de acceso mediante `LoginRequiredMixin` y validación de `request.user.rol` en el método `dispatch()`  

---

### Enrutamiento (`urls.py`)
Configurado en `apppolizas/urls.py`, define las rutas que mapean URLs a vistas específicas, organizando el acceso a cada funcionalidad del sistema con patrones de URL claros y agrupados por módulo funcional  

---

### Validación de Entrada (`forms.py`)
Proporciona validación de datos y configuración de widgets con reglas de negocio integradas:

- **PolizaForm**: Validación de datos financieros y relaciones.
- **SiniestroForm**: Validación de integridad entre custodio y bien.
- **FacturaForm**: Gestión de cálculos automáticos de impuestos.
- **DocumentoSiniestroForm**: Subida segura de archivos con restricciones  

---

### Interfaz Administrativa
Django Admin proporciona gestión directa de datos con clases `Admin` personalizadas para cada entidad del dominio, permitiendo operaciones CRUD avanzadas para administradores  

---

## Capa de Negocio (`services.py`)

### Orquestación de Reglas de Negocio
Encapsula toda la lógica de negocio mediante clases de servicio estáticas:

#### AuthService
- **login_universal()**: Autenticación web con sesiones Django (*services.py:30-46*).
- **login_analista()**: JWT para API con expiración de 2 horas (*services.py:49-74*).

#### PolizaService
- Validación: `prima_total >= prima_base` (*services.py:87-88*).
- Generación automática de notificaciones al crear pólizas (*services.py:93-107*).

#### SiniestroService
- Validación de póliza activa antes de crear siniestro (*services.py:160-163*).
- Notificaciones automáticas al registrar nuevos siniestros (*services.py:168-179*).

#### FiniquitoService
- Fórmula: `valor_final = valor_reclamo - deducible - depreciacion` (*services.py:361-365*).
- Transacciones atómicas para garantizar consistencia (*services.py:381-391*).

#### DocumentoService
- Extensiones permitidas: **PDF, JPG, JPEG, PNG** (*services.py:233-235*).
- Tamaño máximo: **5MB** con validación de tipo MIME (*services.py:254-262*).

---

## Capa de Acceso a Datos (`repositories.py`)

### Patrón Repository
Implementa abstracción de base de datos mediante clases estáticas que encapsulan operaciones CRUD y consultas especializadas:

- **PolizaRepository**: Operaciones CRUD con ordenamiento por fecha de registro.
- **SiniestroRepository**: Consultas especializadas por póliza y creación controlada.
- **DocumentoRepository**: Integración con MinIO para almacenamiento de archivos.
- **UsuarioRepository**: Manejo de autenticación y gestión de usuarios.

Cada repositorio encapsula consultas Django ORM y maneja excepciones `DoesNotExist` de forma centralizada.

---

## Capa de Persistencia

### Modelos de Dominio (`models.py`)
Define la estructura de datos con relaciones y validaciones:

- **Usuario**: Extiende `AbstractUser` con roles específicos del dominio.
- **Poliza**: Entidad central con relaciones a aseguradora, broker y usuario gestor.
- **Siniestro**: Vinculado a póliza, custodio y bien afectado con máquina de estados.
- **Bien**: Activos fijos con validación de límite por custodio.

---

### Base de Datos
MySQL como motor principal con configuración de modo transaccional estricto `STRICT_TRANS_TABLES` para garantizar integridad de datos.

---

## Servicios Externos

### MinIO
Almacenamiento de objetos S3-compatible para documentos y evidencias:

- **Bucket**: `expedientes-siniestros` configurado como público.
- Rutas dinámicas por ID de siniestro para organización.
- Configurado mediante `django-storages`.

### Email
Servicio de notificaciones automáticas integrado en la capa de negocio para alertas de facturación, vencimientos y eventos del sistema.

---

## Patrones Arquitectónicos Implementados

### Dependencias Unidireccionales
El sistema aplica dependencias estrictas:

- **Views → Services**: Las vistas solo llaman métodos de servicio.
- **Services → Repositories**: Los servicios orquestan operaciones.
- **Repositories → Models**: Los repositorios encapsulan ORM.
- **Models → Sistemas Externos**: Persistencia en MySQL y MinIO.

---

### Configuración Centralizada
`settings.py` define conexiones a bases de datos, servicios externos, middleware y autenticación dual, proporcionando un punto único de configuración para todo el sistema.


  
# Diagrama de Paquetes
<img width="1268" height="1261" alt="image" src="https://github.com/user-attachments/assets/fd40209d-2f36-4e9f-81fc-573c0bf1dfd2" />

# Descripción del Diagrama de Paquetes

El sistema de gestión de pólizas y siniestros implementa una **arquitectura de tres capas estricta** con separación de responsabilidades, construida sobre el framework **Django**.  
Esta estructura garantiza **mantenibilidad, testabilidad y escalabilidad** del código.

---

## Capa de Presentación

### `views.py` - Controladores HTTP
Contiene todas las vistas Django que manejan las solicitudes HTTP y respuestas, implementando el patrón MVC de Django.

#### Vistas Principales
- **LoginView**: Maneja autenticación universal con redirección según rol de usuario (*urls.py:16*).
- **DashboardAdminView / DashboardAnalistaView**: Paneles especializados con diferentes niveles de acceso.
- **PolizaListView**: Gestión CRUD completa de pólizas con paginación y filtros.
- **SiniestroListView**: Procesamiento del ciclo de vida completo de siniestros.
- **FiniquitoCreateView**: Liquidación final con cálculos automáticos y validaciones.

#### Control de Acceso
Cada vista implementa control de acceso basado en roles mediante `LoginRequiredMixin` y validación de `request.user.rol` en el método `dispatch()`.

---

### `forms.py` - Validación de Entrada
Proporciona validación de datos y configuración de widgets con reglas de negocio integradas.

#### Formularios Clave
- **PolizaForm**: Validación de datos financieros y relaciones entre entidades.
- **SiniestroForm**: Validación de integridad referencial entre custodio y bien afectado.
- **FacturaForm**: Gestión automática de cálculos de impuestos y descuentos.
- **DocumentoSiniestroForm**: Subida segura de archivos con validación de tipo y tamaño.

---

### `urls.py` - Enrutamiento
Configurado en `apppolizas/urls.py`, define las rutas que mapean URLs a vistas específicas, organizando el acceso a cada funcionalidad del sistema con patrones de URL claros y agrupados por módulo funcional  
*urls.py:1-41*.

---

## Capa de Lógica de Negocio

### `services.py` - Orquestación de Reglas de Negocio
Encapsula toda la lógica de negocio mediante clases de servicio estáticas que implementan el patrón **Service Layer**.

#### Servicios Principales
- **AuthService**: Autenticación dual (sesión para web y JWT para API) con validación de credenciales y roles.
- **PolizaService**: Gestión del ciclo de vida de pólizas con validaciones financieras.
- **SiniestroService**: Procesamiento de siniestros con máquina de estados y reglas de negocio.
- **DocumentoService**: Validación y subida de archivos con restricciones de seguridad.
- **FiniquitoService**: Liquidación con transacciones atómicas y cálculos financieros.

#### Validaciones Críticas
- Validación financiera: `prima_total >= prima_base`.
- Generación automática de notificaciones al crear pólizas.
- Validación de póliza activa antes de crear siniestro.

---

## Capa de Acceso a Datos

### `repositories.py` - Abstracción de Base de Datos
Implementa el patrón **Repository** para acceso a datos mediante clases estáticas que encapsulan operaciones CRUD y consultas especializadas.

#### Repositorios Implementados
- **PolizaRepository**: Operaciones CRUD con ordenamiento por fecha de registro.
- **SiniestroRepository**: Consultas especializadas por póliza y creación controlada.
- **UsuarioRepository**: Manejo de autenticación y gestión de usuarios.
- **DocumentoRepository**: Integración con MinIO para almacenamiento de archivos.

Cada repositorio encapsula consultas Django ORM y maneja excepciones `DoesNotExist` de forma centralizada.

---

## Modelos de Dominio

### `models.py` - Definición de Entidades
Define la estructura de datos y relaciones con validaciones integradas.

#### Entidades Principales
- **Usuario**: Extiende `AbstractUser` con roles específicos del dominio (ADMINISTRADOR, ANALISTA, GERENTE, SOLICITANTE).
- **Poliza**: Entidad central con relaciones a aseguradora, broker y usuario gestor.
- **Siniestro**: Vinculado a póliza, custodio y bien afectado con máquina de estados.
- **Bien**: Activos fijos con validación de límite por custodio.

---

### `migrations/` - Evolución del Esquema
Gestiona la evolución de la base de datos mediante migraciones Django que definen la creación inicial de todas las tablas con sus relaciones y restricciones.

---

## Configuración del Proyecto

### `settings.py` - Configuración Central
Define conexiones a bases de datos y servicios externos, proporcionando un punto único de configuración para todo el sistema  
*settings.py:79-91*.

#### Configuraciones Clave
- **MySQL**: Base de datos principal con modo transaccional estricto `STRICT_TRANS_TABLES` (*settings.py:87-89*).
- **MinIO**: Almacenamiento de objetos compatible con S3 para documentos.
- **Middleware**: Pipeline de procesamiento de solicitudes con seguridad y autenticación.
- **Autenticación**: Configuración dual (sesión + JWT) con modelo de usuario personalizado.

---

### `manage.py` - Utilidad de Administración
Script de Django para tareas administrativas como migraciones, creación de superusuario y ejecución del servidor de desarrollo  
*manage.py:8-19*.

---

## Dependencias Externas

### MySQL
Base de datos relacional principal con modo estricto `STRICT_TRANS_TABLES` para garantizar integridad de datos.

### MinIO
Almacenamiento S3-compatible para documentos de siniestros en el bucket `expedientes-siniestros` con configuración de acceso público  
*settings.py:149-170*.

---

## Flujo de Dependencias y Reglas de Arquitectura
El sistema aplica dependencias unidireccionales estrictas:

- **Views → Services**: Las vistas solo llaman métodos de servicio, nunca repositorios directamente.
- **Services → Repositories**: Los servicios orquestan operaciones a través de repositorios.
- **Repositories → Models**: Los repositorios encapsulan toda interacción con Django ORM.
- **Models → MySQL/MinIO**: Los modelos persisten datos en sistemas externos.

Esto garantiza separación de *concerns* y facilita pruebas unitarias mediante *mocks* de dependencias.

---

## Notas

### Ventajas Arquitectónicas
La estructura modular del sistema permite:

- **Escalabilidad horizontal**: Cada capa puede escalarse independientemente.
- **Mantenimiento simplificado**: Responsabilidades bien definidas por capa.
- **Testabilidad**: Dependencias inyectadas facilitan pruebas unitarias.
- **Integridad arquitectónica**: Impide accesos directos no autorizados a la base de datos desde las vistas o uso del ORM desde los servicios.







