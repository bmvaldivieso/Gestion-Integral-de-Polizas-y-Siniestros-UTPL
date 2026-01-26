# Diagrama de clases
<img width="1838" height="1514" alt="image" src="https://github.com/user-attachments/assets/e89d0dbd-02cb-4419-8bc1-5eb4dfded1b6" />


Este es un Diagrama de Clases UML diseñado para un sistema de gestión de seguros, siniestros y pólizas. 
El modelo centraliza la relación entre los activos asegurados, las entidades legales y los procesos financieros asociados.

# 1. Gestión de Pólizas y Entidades

## Entidad Central – Póliza

La clase **Poliza** funciona como el agregado raíz del dominio de seguros, conteniendo información contractual completa.  
`models.py:169-198`

**Características principales:**
- **Datos contractuales**: número único, vigencia, montos asegurados y primas.
- **Relaciones obligatorias**:  
  - **Aseguradora** (`PROTECT`)  
  - **Broker** (`PROTECT`)  
  para garantizar la integridad referencial.
- **Control de estado**: campos `estado` y `renovable` para la gestión del ciclo de vida.
- **Asignación de gestión**: relación opcional con **Usuario** gestor.

## Entidades Externas

### Aseguradora
Compañías de seguros con RUC único y datos de contacto.  
`models.py:43-51`

### Broker
Intermediarios con correo electrónico para notificaciones automáticas.  
`models.py:54-60`

## Gestión de Usuarios

La clase **Usuario** extiende `AbstractUser` de Django con roles específicos del dominio.  
`models.py:14-35`

**Roles definidos:**
- `ADMINISTRADOR`
- `ANALISTA`
- `GERENTE`
- `SOLICITANTE`

**Extensiones del modelo:**
- Datos adicionales: cédula única, teléfono y estado de cuenta.
- Relaciones múltiples: gestiona pólizas, siniestros y recibe notificaciones.

---

# 2. Gestión de Activos y Custodia

## Entidad Bien

Representa activos fijos con identificación única y estado físico/operativo.  
`models.py:96-161`

**Características:**
- **Identificación**: código único, BAAN V, serie, modelo y marca.
- **Estado dual**:
  - Físico: `Bueno / Regular / Malo`
  - Operativo: `Activo / Inactivo`
- **Validación de integridad**: métodos `clean()` y `save()` personalizados.

## ResponsableCustodio

Personal UTPL responsable de activos con información organizacional completa.  
`models.py:63-88`

**Datos gestionados:**
- Datos personales: nombre completo, identificación única y contacto.
- Ubicación organizacional: departamento, ciudad, edificio y puesto.
- **Relación uno-a-muchos**: un custodio puede administrar múltiples bienes.

---

# 3. Procesamiento de Siniestros

## Entidad Siniestro

Implementa una máquina de estados para el flujo completo de reclamaciones.  
`models.py:215-296`

**Estados definidos:**
REPORTADO → DOCUMENTACIÓN → ENVIADO_ASEGURADORA → REPARACIÓN → LIQUIDADO / RECHAZADO


**Características clave:**
- Validación cruzada: verifica que el bien pertenezca al custodio seleccionado.
- Triángulo relacional: vincula **Poliza**, **Bien** y **ResponsableCustodio**.
- Seguimiento financiero: valor estimado y resultado final (`ARREGLADO / REEMPLAZADO`).

## Finiquito

Liquidación final con cálculos financieros detallados.  
`models.py:304-331`

**Cálculo automático:**
valor_final_pago = valor_total_reclamo - valor_deducible - valor_depreciacion


**Control financiero:**
- Seguimiento de fecha de pago.
- Estado de liquidación.
- **Relación uno-a-uno**: cada siniestro tiene exactamente un finiquito.

## Gestión Documental

- **DocumentoSiniestro**: evidencias clasificadas (`INFORME`, `DENUNCIA`, `FOTOS`, `FACTURA_REPARACIÓN`).  
  `models.py:472-488`
- **Almacenamiento S3**: rutas dinámicas en MinIO estructuradas por ID de siniestro.  
  `models.py:468-469`
- **Limpieza automática**: uso de signals para eliminar archivos huérfanos.

---

# 4. Gestión Financiera y Documental

## Factura

Implementa cálculos automáticos según regulaciones ecuatorianas.  
`models.py:339-416`

**Componentes financieros:**
- Contribuciones legales:
  - 3.5% Superintendencia
  - 0.5% Seguro Campesino
- IVA: 15% sobre base imponible.
- Derechos de emisión: escalables según monto de prima.
- Descuento por pronto pago: 5% si se paga dentro de 20 días.
- **Cálculo automático**: implementado en el método `save()`.

## DocumentoPoliza

Archivos digitales asociados a contratos de póliza con almacenamiento en MinIO.  
`models.py:201-208`

## Sistema de Notificaciones

Alertas automáticas con tipos predefinidos y seguimiento de estado.  
`models.py:422-460`

**Tipos de notificación:**
- `VENCIMIENTO_POLIZA`
- `PAGO_PENDIENTE`
- `SINIESTRO_DEMORA_DOC`
- `REPORTE_EXTERNO`

**Estados:**
- `PENDIENTE`
- `LEIDA`
- `ENVIADA_CORREO`

**Referencia cruzada:** ID de póliza o siniestro relacionado.

---

# 5. Sistema de Reportes Externos

## ReporteExterno

Facilita la recepción de incidentes por usuarios no autenticados.  
`models.py:502-569`

**Datos gestionados:**
- Datos del reportante: nombre, email y teléfono.
- Información del bien: proporcionada por el reportante (puede ser aproximada).
- Clasificación de incidentes:
  - `DAÑOS`
  - `ROBO_HURTO`
  - `INCENDIO`
  - `PÉRDIDA_TOTAL`
  - `DAÑO_LEVE`

**Flujo de aprobación:**
RECIBIDO → REVISADO → CONVERTIDO / RECHAZADO

## Proceso de Conversión

El reporte externo puede convertirse en un siniestro formal manteniendo trazabilidad:

- Validación administrativa por usuario interno.
- Conversión controlada mediante relación `OneToOne` con **Siniestro**.
- Auditoría completa: observaciones administrativas y fecha de revisión.
- Trazabilidad bidireccional: `siniestro.reporte_origen`.

---

# Patrones de Diseño Implementados

## Validaciones de Negocio
- Integridad referencial: validación cruzada entre bien y custodio en `Siniestro.clean()`.  
  `models.py:279-289`
- Cálculos automáticos: lógica de facturación ecuatoriana en `Factura.save()`.  
  `models.py:389-413`

## Gestión de Estado
- Máquinas de estados para siniestros y reportes externos.
- Control del ciclo de vida mediante estados y transiciones validadas.

## Almacenamiento y Persistencia
- Precisión financiera: `DecimalField` con 12 dígitos y 2 decimales.  
  `models.py:182-188`
- Almacenamiento S3 mediante integración con MinIO.
- Limpieza automática: uso de signals para gestión de archivos.


