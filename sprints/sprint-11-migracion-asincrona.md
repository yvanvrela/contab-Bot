# Sprint 11: Migración a Arquitectura Asíncrona (Telegram v20+)

## Objetivo
Actualizar el framework del orquestador (`python-telegram-bot`) desde la versión heredada `13.14` hacia la versión moderna `v20+`. Esto convertirá al bot de un modelo bloqueante (síncrono) a uno multitarea (asíncrono), permitiendo que procese múltiples Excels, consultas y mensajes de usuarios en paralelo sin congelarse.

## Análisis de Impacto
La actualización a la v20+ implica *breaking changes* masivos en la sintaxis de la librería. Afectará principalmente a la inicialización del bot (`main.py`) y a la estructura interna de todos los Controladores (`src/handlers/`).

## Tareas Realizadas

- [x] **Reescritura del Orquestador (`src/main.py`)**
   - Se reemplazó el `Updater` por el nuevo patrón asíncrono `ApplicationBuilder`.
   - Se actualizaron las convenciones de los filtros (de `Filters.regex` a `filters.Regex`).
- [x] **Refactorización de Controladores (`src/handlers/`)**
   - Todos los handlers ahora operan como corrutinas (`async def`).
   - Se introdujo `await` en absolutamente todas las peticiones a la API de Telegram.
- [x] **Adaptación de Manejo de Archivos (`file_handlers.py`)**
   - Se actualizó el flujo de descargas temporales hacia el nuevo método `await file.download_to_drive()`.
- [x] **Compatibilidad con Operaciones Síncronas (Bloqueantes)**
   - Utilizando 4 agentes de programación paralela, analizamos y envolvimos exitosamente todas las interacciones que rompían el Event Loop (como consultas de SQLAlchemy o descargas de *Requests*) inyectándolas en hilos secundarios mediante `await asyncio.to_thread(...)`. 
   - Se creó un sistema ingenioso de "callbacks síncronos-a-asíncronos" (`run_coroutine_threadsafe`) para que las barras de progreso mantengan vivo el feedback visual durante descargas pesadas.

## Estado
**Completado.** El robot ahora cuenta con un modelo multitarea real, escalable y resistente al bloqueo.
