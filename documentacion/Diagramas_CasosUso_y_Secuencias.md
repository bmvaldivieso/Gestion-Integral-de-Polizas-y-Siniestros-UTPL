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








