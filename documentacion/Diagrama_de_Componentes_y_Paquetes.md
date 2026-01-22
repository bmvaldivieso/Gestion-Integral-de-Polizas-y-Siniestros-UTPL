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
