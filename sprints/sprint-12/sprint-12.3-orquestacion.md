# Sprint 12.3: Orquestación (Docker Compose)

## Objetivo
Vincular el contenedor de Python del robot con un contenedor oficial de Selenium (Firefox) mediante `docker-compose.yml`, orquestando la red interna y mapeando volúmenes para garantizar que la base de datos SQLite y las lecturas de los discos compartidos (`Z:`) persistan y funcionen correctamente.

## Tareas Realizadas

- [x] **Creación del `docker-compose.yml`**
   - Se configuró el servicio `selenium` usando `selenium/standalone-firefox:latest`, asignándole el tamaño de memoria seguro (`shm_size: '2g'`) y exponiendo el puerto VNC (7900) para poder espiar lo que hace el bot visualmente desde un navegador.
   - Se configuró el servicio `bot`, construyendo a partir del `Dockerfile` e inyectándole las dependencias (`depends_on: selenium`) y el archivo `.env`.
   - Se forzó la variable dinámica `SELENIUM_URL=http://selenium:4444/wd/hub` para que el bot sobreescriba su lógica de Python y utilice la red local del contenedor.

- [x] **Mapeo de Volúmenes (Persistencia y Red)**
   - Se habilitó la persistencia de SQLite montando `./src/db/config:/app/src/db/config`.
   - Se dejaron plantillas (comentadas) sobre cómo montar los discos de red compartidos `Z:/` hacia la estructura de carpetas interna de Linux.

## Estado
**Completado.** La arquitectura de orquestación está totalmente ensamblada. El bot y su navegador ahora operan en un ecosistema de red virtual unificado, listo para producción.
