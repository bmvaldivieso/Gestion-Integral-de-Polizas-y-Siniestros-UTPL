
# DIAGRAMAS DE CASOS DE USO 



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

<img width="757" height="823" alt="image" src="https://github.com/user-attachments/assets/d337aad0-b244-457e-a406-60468dc9e597" />

Los Reportes Externos permiten que usuarios no autenticados registren de forma preliminar un siniestro, ingresando información básica del reportante, del bien afectado y del incidente.


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

## 7. Reportes Externos (UC07)
La funcionalidad de **Reportes Externos** permite que personas no autenticadas puedan informar la ocurrencia de un incidente o siniestro mediante un formulario web público, sin necesidad de contar con credenciales dentro del sistema.  
Este mecanismo actúa como un canal de entrada preliminar al proceso formal de gestión de siniestros.

### Actores Involucrados

- **Usuario Externo**: Persona ajena al sistema que registra un incidente proporcionando datos básicos del reportante, del bien afectado y del evento ocurrido.
- **Analista**: Usuario interno responsable de revisar, validar y decidir el destino de los reportes externos.
- **Sistema**: Componentes automatizados que realizan validaciones de datos y generan notificaciones automáticas.

### Flujo General del Proceso

1. El usuario externo envía un reporte a través del formulario público.  
2. El sistema valida automáticamente los datos de entrada, como el formato del correo electrónico y el número telefónico.  
3. Al registrarse un nuevo reporte, el sistema notifica automáticamente a los analistas.  
4. El analista revisa los reportes pendientes y puede consultar su información detallada.  
5. Tras la revisión, el analista puede:
   - **Convertir el reporte en un siniestro formal**, integrándolo al flujo oficial del sistema.  
   - **Rechazar el reporte**, registrando observaciones administrativas.  

### Beneficios de la Funcionalidad

- Facilita la recepción temprana de incidentes.  
- Reduce barreras de acceso para usuarios externos.  
- Garantiza control administrativo antes de crear siniestros formales.  
- Asegura trazabilidad completa desde el reporte inicial hasta el siniestro generado.  

 

# Documentación de los Diagramas de Secuencia

## 1. Diagrama de Secuencia: Autenticación de Usuario

<img width="850" height="924" alt="image" src="https://github.com/user-attachments/assets/2b46ad96-7b2d-4fcf-b366-bd2962c3c2c2" />

### Propósito
Este diagrama documenta el flujo de login del sistema, manejando la autenticación de usuarios y redirección basada en roles (admin/analista).

### Actores y Componentes
* **Browser:** Cliente web que inicia la solicitud.
* **LoginView:** Controlador que maneja GET/POST.
* **AuthService:** Servicio de autenticación universal.
* **DjangoAuth:** Sistema de autenticación subyacente.
* **Session:** Gestor de sesiones de Django.

### Flujo Principal
1.  El navegador envía credenciales vía POST a `/login/`.
2.  `LoginView` valida que los campos no estén vacíos.
3.  Se delega a `AuthService.login_universal()` para validación.
4.  `DjangoAuth.authenticate()` verifica credenciales contra la base de datos.
5.  **Si es exitoso:** Se crea la sesión y se retorna JSON con URL de redirección.
6.  **Si falla:** Se retorna error 401 con mensaje descriptivo.

### Reglas de Negocio
* Todos los campos son obligatorios.
* El usuario debe tener un rol asignado (admin/analista).
* **Redirección automática según rol:** * Admin → Dashboard Admin
    * Analista → Dashboard Analista

---

## 2. Diagrama de Secuencia: Creación de Siniestros

<img width="1277" height="1188" alt="image" src="https://github.com/user-attachments/assets/781798a7-4ed5-4e0a-b3e3-4508b06157ab" />

### Propósito
Documenta el proceso completo de creación de siniestros, incluyendo validaciones de integridad de datos y notificaciones automáticas.

### Actores y Componentes
* **Analyst:** Usuario con rol analista que crea el siniestro.
* **SiniestroListView:** Vista que maneja el formulario de creación.
* **SiniestroForm:** Formulario con validaciones específicas.
* **SiniestroService:** Lógica de negocio para creación.
* **SiniestroRepository:** Capa de acceso a datos.
* **DB:** Base de datos MySQL.

### Flujo Principal
1.  El analista envía el formulario POST a `/siniestros/`.
2.  `SiniestroForm` valida datos de entrada.
3.  **Validación específica:** El bien debe pertenecer al custodio seleccionado.
4.  Se filtran solo los campos del modelo `Siniestro`.
5.  `SiniestroService.crear_siniestro()` ejecuta lógica de negocio.
6.  **Validación:** La póliza debe estar activa.
7.  Se crea el registro en base de datos.
8.  Se genera notificación automática.
9.  Redirección con mensaje de éxito.

### Validaciones Críticas
* Integridad relacional bien-custodio.
* Estado operativo del bien (debe estar **ACTIVO**).
* Póliza debe estar activa y vigente.

---

## 3. Diagrama de Secuencia: Flujo de Estados de Siniestro

<img width="1640" height="2043" alt="image" src="https://github.com/user-attachments/assets/3a064974-bf35-44f8-870a-fae9d824fcd5" />


### Propósito
Representa la máquina de estados de 4 fases del ciclo de vida de un siniestro: 
`REPORTADO` → `ENVIADO_ASEGURADORA` → `REPARACIÓN` → `LIQUIDADO`.

### Actores y Componentes
* **Analyst:** Usuario que ejecuta las transiciones.
* **EnviarAseguradoraView:** Cambia estado a ENVIADO_ASEGURADORA.
* **RepararSiniestroView:** Maneja reparación o reemplazo.
* **FiniquitoCreateView:** Procesa liquidación final.
* **Siniestro:** Modelo persistente con estado.
* **DB:** Base de datos con transacciones atómicas.

### Flujo por Estados

#### Estado REPORTADO → ENVIADO_ASEGURADORA
1.  Analista envía POST a `/siniestros/{id}/enviar_aseguradora/`.
2.  **Validación:** Estado actual debe ser `REPORTADO`.
3.  Se actualiza estado a `ENVIADO_ASEGURADORA`.
4.  Confirmación al usuario.

#### Estado ENVIADO_ASEGURADORA → REPARACIÓN
1.  Analista envía POST a `/siniestros/{id}/reparar/`.
2.  **Validación:** Estado debe ser `ENVIADO_ASEGURADORA`.
3.  **Opción ARREGLADO:** Simple actualización de estado.
4.  **Opción REEMPLAZADO:** Transacción atómica compleja.
    * Marcar bien antiguo como **INACTIVO**.
    * Crear nuevo bien con código suffix "-R".
    * Actualizar referencia en siniestro.

#### Estado REPARACIÓN → LIQUIDADO
1.  Analista envía POST a `/siniestros/{id}/finiquitar/`.
2.  `FiniquitoService.liquidar_siniestro()` calcula valores.
3.  Se crea registro de finiquito.
4.  `Siniestro` cambia a estado `LIQUIDADO`.
5.  Se muestra valor final a pagar.

### Reglas de Negocio
* Las transiciones son unidireccionales.
* Cada estado tiene validaciones específicas.
* El reemplazo usa transacciones atómicas para consistencia.

---

## 4. Diagrama de Secuencia: Gestión de Pólizas

<img width="1128" height="1229" alt="image" src="https://github.com/user-attachments/assets/b6450830-4b12-439b-bd0e-8c00f7c8ae49" />


### Propósito
Documenta la creación de pólizas de seguro con asignación automática de usuario gestor y validaciones financieras.

### Actores y Componentes
* **Analyst:** Usuario que gestiona pólizas.
* **PolizaListView:** Vista para creación y listado.
* **PolizaForm:** Formulario con validaciones de campos.
* **PolizaService:** Lógica de negocio de pólizas.
* **DB:** Base de datos persistente.

### Flujo Principal
1.  Analista envía formulario POST a `/polizas/`.
2.  `PolizaForm` valida todos los campos.
3.  **Inyección automática:** `request.user` como `usuario_gestor`.
4.  `PolizaService.crear_poliza()` ejecuta validaciones.
5.  **Validación financiera:** `prima_total >= prima_base`.
6.  Creación del registro en base de datos.
7.  Generación de notificación automática.
8.  Redirección con mensaje de éxito.

### Validaciones Importantes
* Consistencia financiera entre primas.
* Fechas de vigencia válidas.
* Unicidad del número de póliza.
* Relaciones válidas con aseguradora y broker.

### Características Especiales
* Asignación automática del usuario logueado como gestor.
* Notificación automática al crear póliza.
* Solo usuarios con rol "analista" pueden gestionar pólizas.

---

## 5. Diagrama de Secuencia: Gestión de Documentos

<img width="1408" height="1388" alt="image" src="https://github.com/user-attachments/assets/0ce741c6-cd8e-4961-9aff-21457b798a85" />

### Propósito
Maneja la subida de evidencia documental a MinIO con validaciones de seguridad y metadatos en MySQL.

### Actores y Componentes
* **Analyst:** Usuario que sube documentos.
* **SubirEvidenciaView:** Vista para upload de archivos.
* **DocumentoForm:** Validador de archivos y metadatos.
* **DocumentoService:** Lógica de gestión documental.
* **MinIO:** Almacenamiento de objetos distribuido.
* **DB:** MySQL para metadatos.

### Flujo Principal
1.  Analista selecciona archivo y completa formulario.
2.  POST a `/siniestros/{id}/subir_evidencia/`.
3.  `DocumentoForm` valida archivo y metadatos.
4.  `DocumentoService.subir_evidencia()` ejecuta validaciones:
    * Siniestro existe y no está `LIQUIDADO`.
    * Extensión permitida (`.pdf`, `.jpg`, `.png`).
    * Tamaño máximo 5MB.
5.  Upload del archivo a **MinIO**.
6.  Guardado de metadatos en **MySQL**.
7.  Redirección con confirmación.

### Validaciones de Seguridad
* El siniestro debe existir y no estar liquidado.
* Extensiones permitidas: PDF, JPG, PNG.
* Tamaño máximo: 5MB.
* Solo usuarios analistas pueden subir documentos.

### Características Técnicas
* Almacenamiento en MinIO (S3-compatible).
* Metadatos en MySQL para búsquedas.
* URL generada para acceso al archivo.
* Integración con expediente digital del siniestro.

---

## 6. Diagrama de Secuencia: Gestión de Usuarios (Admin)

<img width="896" height="1814" alt="image" src="https://github.com/user-attachments/assets/eaef1e99-eef8-4f70-a48b-c49b5edda574" />

### Propósito
Implementa CRUD completo para gestión de usuarios del sistema, accesible solo por administradores.

### Actores y Componentes
* **Admin:** Usuario con rol administrador.
* **UsuarioCRUDView:** API REST para gestión de usuarios.
* **UsuarioRepository:** Capa de acceso a datos de usuarios.
* **DB:** Base de datos persistente.

### Operaciones CRUD

#### `GET /api/usuarios/` (Listar)
1.  Admin solicita lista de usuarios.
2.  `UsuarioRepository.get_all_usuarios()` ejecuta consulta.
3.  Retorna JSON con array de usuarios.

#### `POST /api/usuarios/` (Crear)
1.  Admin envía JSON con datos de nuevo usuario.
2.  `UsuarioRepository.create_usuario()` crea registro.
3.  Validación de unicidad de username y email.
4.  Retorna ID del usuario creado.

#### `PUT /api/usuarios/{id}/` (Actualizar)
1.  Admin envía JSON con datos actualizados.
2.  `UsuarioRepository.update_usuario()` modifica registro.
3.  Validación de existencia del usuario.
4.  Retorna confirmación de actualización.

#### `DELETE /api/usuarios/{id}/` (Eliminar)
1.  Admin solicita eliminación.
2.  `UsuarioRepository.delete_usuario()` elimina registro.
3.  Protección contra eliminación de usuarios con datos relacionados.
4.  Retorna confirmación de eliminación.

### Reglas de Seguridad
* Solo usuarios con rol "admin" pueden acceder.
* Todas las operaciones requieren autenticación.
* Validaciones de integridad referencial.
* CSRF exempt para API endpoints.










