# Sprint 9: Gestor de Archivos Temporales y Manejo de Basura

## Objetivo
Solucionar el bug de acumulación de archivos residuales (Excel y HTML) en la raíz del proyecto. Se implementará un directorio dedicado para el procesamiento temporal y rutinas defensivas que garanticen el borrado de los mismos, sin importar si ocurren errores durante el parseo.

## Análisis del Bug
La función `file_manager` en `src/handlers/file_handlers.py` tiene un diseño lineal. Si la librería de Pandas falla al leer el Excel (por un formato inválido) o la red se desconecta antes del envío, el programa arroja una excepción y aborta la ejecución antes de alcanzar las últimas líneas donde residen los comandos `os.remove()`. Esto resulta en archivos permanentemente huérfanos.

## Tareas Realizadas

- [x] **Directorio Dedicado (`src/temp/`)**
   - Se creó la carpeta `src/temp/` y se bloqueó en el archivo `.gitignore`.
- [x] **Refactorización Defensiva (`try...finally`)**
   - Se reescribió `file_manager` en `src/handlers/file_handlers.py`.
   - Si un usuario manda un Excel malicioso o dañado, el bot ahora le responde amablemente (`"❌ Ocurrió un error al procesar tu planilla..."`) en lugar de ignorarlo y crashear silenciosamente.
   - El bloque `finally` obliga al sistema operativo a destruir los archivos temporales (`os.remove()`) pase lo que pase, evitando que el servidor se llene de archivos basura.
- [x] **Redirección de Rutas**
   - El bot ahora llama a `telegram_file.download(custom_path=...)` obligándolo a descargar en la carpeta temporal.
   - La función matemática en `utils/html_convert.py` fue modificada para recibir el parámetro `out_dir`, inyectando el `.html` resultante directo a la cuarentena de `temp/`.

## Estado
**Completado.** La función de procesamiento de facturas R-90 es ahora invulnerable a cuelgues y totalmente limpia.
