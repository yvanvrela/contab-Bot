# Sprint 8: Búsqueda Mágica de RUCs y Nombres

## Objetivo
Mejorar la Experiencia de Usuario (UX) permitiendo que Benito detecte automáticamente cédulas, RUCs o nombres enviados en el chat general sin depender de la fricción del comando `/buscarci`. Además, incorporar el motor de búsqueda por similitud de nombres.

## Análisis
Actualmente el flujo es estricto: `/buscarci` -> Esperar mensaje de Benito -> Ingresar Número -> Recibir respuesta.
Queremos lograr un modelo "Spotlight": Escribir un número o nombre en el chat y recibir los datos de inmediato, aprovechando la velocidad de SQLite. El comando `/buscarci` antiguo se mantendrá intacto por retrocompatibilidad.

## Tareas Realizadas

- [x] **Implementar "Búsqueda Instantánea por Número"**
   - Se creó el handler `instant_search_number` en `src/handlers/ruc_handlers.py`.
   - Se capturó mediante Regex en `main.py` para ignorar la fricción del comando `/buscarci`.
   - Ahora si un usuario escribe un número puro, el bot salta directamente a la consulta instantánea.

- [x] **Implementar "Búsqueda Mágica por Nombre"**
   - Se añadió `search_by_name` usando `LIKE` en `contribuyentes_repository.py`.
   - Se creó `instant_search_name` en `src/handlers/ruc_handlers.py`.
   - Se configuró el Regex `(?i)^(?:buscar|ruc(?: de)?)\s+(.+)` para activarlo.
   - El resultado se forza visualmente con `.upper()` para garantizar que todos los nombres y estados devueltos en el chat estén en mayúsculas como pidió el usuario.

## Estado
**Completado.** La fluidez al usar el bot mejoró masivamente.
