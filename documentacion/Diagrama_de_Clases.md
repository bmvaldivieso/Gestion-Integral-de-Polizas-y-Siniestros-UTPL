# Diagrama de clases
<img g width="1080" height="990" alt="image" src="https://github.com/user-attachments/assets/a5c2eeef-748c-4a9a-8764-a510068db8f6" />

Este es un Diagrama de Clases UML diseñado para un sistema de gestión de seguros, siniestros y pólizas. 
El modelo centraliza la relación entre los activos asegurados, las entidades legales y los procesos financieros asociados.

# 1. Gestión de Pólizas y Actores
**Póliza**: Es la clase central. Contiene información sobre montos asegurados, vigencia y primas. Se relaciona con un Broker y una Aseguradora.

**Bien**: Representa el activo físico asegurado (marca, modelo, serie). Cada bien tiene un Responsable Custodio asignado.

**Usuario**: Representa a las personas dentro del sistema, vinculado tanto a las pólizas como a la recepción de notificaciones.

# 2. Procesamiento de Siniestros
**Siniestro**: Se activa cuando ocurre un evento cubierto por la póliza. Registra la causa, la cobertura aplicada y el valor estimado del reclamo.

**DocumentoSiniestro**: Almacena los archivos y evidencias necesarios para respaldar un reclamo.

**Finiquito**: Es el paso final del siniestro, donde se detallan los pagos realizados, deducciones y el valor final liquidado.

# 3. Documentación y Finanzas
**Factura**: Maneja la parte contable de las pólizas, incluyendo cálculos de impuestos (IVA), retenciones, descuentos por pronto pago y contribuciones legales.

**DocumentoPoliza**: Archivos adjuntos digitales relacionados específicamente con el contrato de la póliza.

**Notificación**: Un módulo para rastrear las alertas enviadas a los usuarios (por correo o estado de sistema).
