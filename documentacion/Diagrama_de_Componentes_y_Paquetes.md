# Diagramade Componentes
<img width="1080" height="990" alt="image" src="https://github.com/user-attachments/assets/db006228-b996-4aae-b8b7-dd898bef2f67" />

# Descripción del Diagrama de Componentes
El diagrama representa la arquitectura de 3 capas del sistema de gestión integral de pólizas y siniestros, implementada con Django siguiendo patrones de diseño estrictos.

## Arquitectura General y Flujo
El sistema sigue un flujo unidirectional donde el cliente envía solicitudes HTTP que atraviesan las capas en orden: **Presentación** → **Negocio** → **Datos**. Esta separación garantiza que cada capa tenga responsabilidades bien definidas sin violar las dependencias.

### Capa de Presentación
- **Views**: Clases como `LoginView`, `PolizaListView`, `SiniestroListView` manejan solicitudes HTTP y coordinan con la capa de negocio. Implementan validación de formularios y control de acceso mediante `LoginRequiredMixin` y verificación de roles en el método `dispatch()`.
  
- **URL Routing**: Configurado en `apppolizas/urls.py`, define las rutas que mapean URLs a vistas específicas, organizando el acceso a cada funcionalidad del sistema.
  
- **Templates**: Archivos HTML que renderizan la interfaz de usuario, recibiendo contexto desde las vistas para mostrar datos y formularios.

### Capa de Negocio (Services)
- **AuthService**: Gestiona autenticación dual (sesiones para web y JWT para API) con validación de credenciales y roles.
  
- **PolizaService**: Implementa lógica de negocio para gestión de pólizas, incluyendo validaciones de negocio y generación automática de notificaciones.
  
- **SiniestroService**: Orquesta el flujo completo de siniestros, validando reglas de negocio como que la póliza esté activa antes de crear un siniestro.
  
- **FiniquitoService**: Procesa liquidaciones con cálculos financieros y transacciones atómicas para garantizar consistencia de datos.

### Capa de Datos
- **Models**: Entidades como `Usuario`, `Poliza`, `Siniestro` definen la estructura de datos con relaciones y validaciones.
  
- **Repositories**: Clases como `PolizaRepository` y `SiniestroRepository` abstraen el acceso a datos, encapsulando operaciones CRUD e interacción con el ORM de Django.
  
- **Database**: MySQL como motor de base de datos con configuración de modo transaccional estricto.

## Servicios Externos
- **MinIO**: Almacenamiento de objetos S3-compatible para documentos y evidencias de siniestros, configurado mediante `django-storages`.
  
- **Email**: Servicio de notificaciones automáticas integrado en la capa de negocio para alertas de facturación y eventos del sistema.

<img width="1268" height="1261" alt="image" src="https://github.com/user-attachments/assets/fd40209d-2f36-4e9f-81fc-573c0bf1dfd2" />

# Arquitectura General del Sistema

El sistema de gestión de pólizas y siniestros implementa una **arquitectura de tres capas estricta** con separación de responsabilidades, construida sobre el framework **Django**.  
Esta estructura garantiza **mantenibilidad, testabilidad y escalabilidad** del código.

---

## Capa de Presentación

### `views.py` - Controladores HTTP
Contiene todas las vistas Django que manejan las solicitudes HTTP y respuestas (`views.py:1-30`).  
Vistas principales:
- **LoginView**: Maneja la autenticación de usuarios  
- **DashboardAdminView / DashboardAnalistaView**: Paneles de control según rol  
- **PolizaListView**: Gestión CRUD de pólizas  
- **SiniestroListView**: Gestión de siniestros  
- **FiniquitoCreateView**: Proceso de liquidación de siniestros  

Cada vista implementa control de acceso basado en roles mediante `LoginRequiredMixin` y validación de `request.user.rol` (`views.py:85-91`).

### `forms.py` - Validación de Entrada
Proporciona validación de datos y configuración de widgets (`forms.py:18-79`).  
Formularios clave:
- **PolizaForm**: Validación de datos de pólizas con reglas de negocio  
- **SiniestroForm**: Validación de integridad entre custodio y bien  
- **FacturaForm**: Gestión de facturación  
- **DocumentoSiniestroForm**: Subida de archivos  

---

## Capa de Lógica de Negocio

### `services.py` - Orquestación de Reglas de Negocio
Encapsula toda la lógica de negocio (`services.py:72-135`).  
Servicios principales:
- **AuthService**: Autenticación dual (sesión y JWT) (`services.py:21-70`)  
- **PolizaService**: Gestión del ciclo de vida de pólizas con validaciones financieras  
- **SiniestroService**: Procesamiento de siniestros con reglas de negocio  
- **DocumentoService**: Validación y subida de archivos con restricciones de seguridad  

Validaciones críticas:
- `prima_total >= prima_base` (`services.py:80-84`)  
- Generación de notificaciones automáticas (`services.py:88-103`)  

---

## Capa de Acceso a Datos

### `repositories.py` - Abstracción de Base de Datos
Patrón **Repository** para acceso a datos mediante clases estáticas (`repositories.py:47-75`).  
Repositorios implementados:
- **PolizaRepository**: Operaciones CRUD para pólizas  
- **SiniestroRepository**: Consultas especializadas de siniestros  
- **UsuarioRepository**: Manejo de usuarios  
- **DocumentoRepository**: Integración con MinIO para almacenamiento de archivos  

Cada repositorio encapsula consultas Django ORM y maneja excepciones `DoesNotExist` (`repositories.py:55-59`).

---

## Modelos de Dominio

### `models.py` - Definición de Entidades
Define la estructura de datos y relaciones (`models.py:173-202`).  
Entidades principales:
- **Usuario**: Extiende `AbstractUser` con roles específicos (`models.py:14-35`)  
- **Poliza**: Entidad central con relaciones a aseguradora, broker y usuario gestor  
- **Siniestro**: Vinculado a póliza, custodio y bien afectado (`models.py:219-300`)  
- **Bien**: Activos fijos con validación de límite por custodio (`models.py:96-165`)  

### `migrations/` - Evolución del Esquema
Gestiona la evolución de la base de datos (`0001_initial.py:268-322`).  
Define la creación inicial de todas las tablas con sus relaciones y restricciones.

---

## Configuración del Proyecto

### `settings.py` - Configuración Central
Define conexiones a bases de datos y servicios externos.  
Configuraciones clave:
- **MySQL**: Base de datos principal con modo transaccional estricto  
- **MinIO**: Almacenamiento de objetos compatible con S3 para documentos  
- **Middleware**: Pipeline de procesamiento de solicitudes  
- **Autenticación**: Configuración dual (sesión + JWT)  

---

## Dependencias Externas

- **MySQL**: Base de datos relacional principal con modo estricto `STRICT_TRANS_TABLES`  
- **MinIO**: Almacenamiento S3-compatible para documentos de siniestros en el bucket `expedientes-siniestros`  

---

## Flujo de Dependencias y Reglas de Arquitectura

El sistema **enforce dependencias unidireccionales estrictas**:

- **Views → Services**: Las vistas solo llaman métodos de servicio, nunca repositorios directamente  
- **Services → Repositories**: Los servicios orquestan operaciones a través de repositorios  
- **Repositories → Models**: Los repositorios encapsulan toda interacción con Django ORM  
- **Models → MySQL/MinIO**: Los modelos persisten datos en sistemas externos  

Esto garantiza **separación de concerns** y facilita pruebas unitarias mediante mocks de dependencias.

---

## Notes

La estructura modular del sistema permite:
- **Escalabilidad horizontal**  
- **Mantenimiento simplificado**  
- **Responsabilidades bien definidas por capa**  

La arquitectura impide accesos directos no autorizados a la base de datos desde las vistas o uso del ORM desde los servicios.



