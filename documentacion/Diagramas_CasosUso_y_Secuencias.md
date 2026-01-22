<img width="700" height="639" alt="image" src="https://github.com/user-attachments/assets/9f39029e-1d04-4bcb-820c-7162221acecb" />


Representación visual de las funcionalidades administrativas. Incluye la generalización en la gestión de usuarios y la relación de inclusión (<<include>>) necesaria para compilar estadísticas al generar reportes.


<img width="704" height="681" alt="image" src="https://github.com/user-attachments/assets/0a9eee55-419f-43a0-90f8-567961254621" />


Representación de la lógica de seguridad y navegación inicial. El caso de uso base "Iniciar sesión" orquesta la validación de credenciales y determina la vista de destino según el rol del actor, asegurando la separación de privilegios desde el acceso.


<img width="700" height="705" alt="image" src="https://github.com/user-attachments/assets/a5a1e7f0-f779-4c6c-af8e-35bfb5183bb9" />


Representación de las interfaces de administración del catálogo de seguros. El diagrama modela las interacciones directas del actor Analista con el sistema para el mantenimiento de registros de pólizas y la trazabilidad hacia los siniestros asociados.


<img width="718" height="744" alt="image" src="https://github.com/user-attachments/assets/83faaa1e-c199-4277-a319-b9f81657ab6d" />


Representación visual de la gestión operativa. El modelo encapsula la lógica de negocio al forzar la inclusión del caso de uso "Validar estado actual" cada vez que se intenta avanzar en el flujo del siniestro, asegurando la integridad de la máquina de estados.


<img width="700" height="545" alt="image" src="https://github.com/user-attachments/assets/d1f1671f-558d-4ac4-aeb8-8ee5511ce72f" />


Representación de la gestión de archivos binarios y la integración con servicios externos. El diagrama modela la dependencia del sistema con el actor minIO storage para la persistencia de datos y aisla la lógica de verificación de ficheros (formatos y peso) mediante una relación de inclusión.


<img width="700" height="664" alt="image" src="https://github.com/user-attachments/assets/744a2da4-bfdd-460d-a405-699ab66580e8" />


Representación del flujo de cierre financiero. El diagrama modela la atomicidad de la operación "Liquidar siniestro", la cual encapsula reglas de negocio financieras y de integridad de datos mediante dependencias de inclusión, asegurando que no se procese ningún pago sin el documento de respaldo correspondiente.



# Especificación de Modelado de Casos de Uso

Esta sección detalla la arquitectura funcional del sistema, desglosada por módulos críticos. Los diagramas ilustran las interacciones entre los actores (Analista, Administrador) y los componentes lógicos, destacando las dependencias (<<include>>) y extensiones (<<extend>>) que gobiernan las reglas de negocio.

## 1. Módulo de Autenticación y Control de Acceso (UC01)

Este módulo actúa como la puerta de entrada segura al sistema, implementando un control de acceso basado en roles (RBAC) para segregar las funciones administrativas de las operativas.



### Lógica del Proceso
El caso de uso "Iniciar Sesión" funciona como un orquestador que:
1. **Valida Credenciales:** Ejecuta obligatoriamente la verificación contra la base de datos de usuarios.
2. **Redirección Inteligente:** Dependiendo del rol detectado, extiende el flujo hacia el Dashboard correspondiente:
   * **Administradores:** Acceso a gestión de usuarios y reportes globales.
   * **Analistas:** Acceso a gestión de pólizas y siniestros.

## 2. Gestión del Ciclo de Vida de Siniestros (UC02)

Módulo central operativo que permite al Analista administrar el flujo de trabajo de un siniestro desde su reporte hasta su resolución.



### Reglas de Negocio Implementadas
El diseño asegura la integridad del flujo mediante validaciones de estado previas a cualquier transición crítica.

| Acción | Restricción / Dependencia | Tipo |
| :--- | :--- | :--- |
| **Enviar a Aseguradora** | Requiere validar que el estado actual sea REPORTADO. | <<include>> |
| **Registrar Reparación** | Requiere validar que el siniestro haya sido aprobado previamente. | <<include>> |

## 3. Administración de Pólizas (UC03)

Provee las interfaces necesarias para que el Analista mantenga el catálogo de pólizas actualizado, sirviendo como base de datos maestra para la validación de siniestros.



### Capacidades del Módulo
* **CRUD Completo:** Creación, lectura, actualización y eliminación de registros de pólizas.
* **Trazabilidad:** La vista de detalles permite visualizar no solo los datos de la póliza, sino todos los siniestros asociados históricamente a ella, facilitando auditorías rápidas.

## 4. Módulo de Liquidación y Cierre Financiero (UC04)

Gestiona la fase crítica de finalización del siniestro. El diseño garantiza la integridad financiera y legal mediante operaciones atómicas.


### Especificaciones del Flujo
La operación "Liquidar Siniestro" orquesta tres validaciones obligatorias para evitar fraudes o errores:
1. **Validación de Integridad:** Verifica que no exista una liquidación previa (Anti-Duplicidad).
2. **Cálculo Automático:** Aplica la fórmula Max(0, Reclamo - Deducible - Depreciación) sin intervención manual.
3. **Respaldo Legal:** Exige la carga de un Finiquito Firmado como precondición bloqueante.

## 5. Gestión Documental y Almacenamiento (UC05)

Encargado de la persistencia de evidencias digitales, interactuando con sistemas de almacenamiento externo (MinIO) para reducir la carga en la base de datos principal.



### Aspectos Técnicos
* **Validación de Ficheros:** Antes de iniciar la transmisión al servidor, se verifica obligatoriamente el tipo MIME (PDF, JPG, PNG) y el tamaño máximo (5MB).
* **Abstracción de Storage:** El sistema interactúa con el actor externo MinIO Storage, desacoplando la lógica de negocio de la infraestructura de archivos.

## 6. Administración del Sistema (UC06)

Módulo exclusivo para el rol de Administrador, enfocado en el mantenimiento de usuarios y la generación de inteligencia de negocio.



### Funcionalidades Clave
* **Gestión de Usuarios:** Control total (Crear, Editar, Eliminar) sobre los accesos al sistema.
* **Reportaría:** Generación de Reportes Generales en PDF. Este proceso incluye obligatoriamente la compilación de estadísticas globales (siniestros totales, montos pagados, etc.) para ofrecer una visión macro del estado del negocio.









