# Sprint 12.2: Construcción de la Imagen (Dockerfile)

## Objetivo
Definir el entorno empaquetado del sistema operativo, las dependencias de Python y las reglas de ignorado para contenerizar `contabBot` de manera segura y minimalista, sentando las bases para la orquestación.

## Tareas Realizadas

- [x] **Crear el archivo `.dockerignore`**
   - Se ignoraron `venv/`, caché de Python, el archivo local `contabot.db`, y carpetas locales como `.env` y `sprints/` para no engordar la imagen.
- [x] **Crear el `Dockerfile` maestro**
   - Se utilizó `python:3.11-slim`.
   - Se agregaron rutinas `apt-get` para generar el local de idioma `es_ES.utf8` dentro del SO Linux del contenedor, garantizando que los formateos de fechas sigan en español sin tirar *Warnings*.
   - Las variables de entorno para optimización de consola (`PYTHONUNBUFFERED=1`) fueron configuradas.
   - El código copia `requirements.txt` por separado para optimizar la compilación rápida en la capa de caché.

## Estado
**Completado.** La receta para el contenedor del bot principal ha sido escrita de manera segura y eficiente.
