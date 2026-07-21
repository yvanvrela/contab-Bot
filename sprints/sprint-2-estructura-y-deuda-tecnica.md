# Sprint 2: Estructura y Deuda Técnica (Refactorización)

## Objetivo
Mejorar la fiabilidad y mantenibilidad del código arreglando problemas de ejecución y el manejo deficiente de excepciones.

## Tareas Realizadas
- [x] **Manejo de Errores (Bare Excepts)**: Refactorizar `src/marangatu/marangatu.py`. Reemplazar los múltiples bloques `except:` genéricos por excepciones específicas (`TimeoutException`, `NoSuchElementException`, o `Exception as e`) para evitar la ocultación de bugs (silent failures).
- [x] **Limpieza de Consola y Logging**: Integrar formalmente la librería `logging` en reemplazo de los numerosos `print()` dispersos en utilidades como `html_convert.py` y `tests_main.py`.
- [x] **Estandarización de Imports**: Arreglar los conflictos de importaciones relativas vs absolutas para que tanto el Bot, como la API (`src/api`) y los Tests (`tests_main.py`) puedan ejecutarse sin fallar desde el mismo directorio raíz.

## Estado
**Completado.** Se ha reducido enormemente la probabilidad de errores silenciosos. Los tests corren con logs formales y toda la app (Bot + API + Tests) usa un solo origen de ejecución uniforme (`src/`).
