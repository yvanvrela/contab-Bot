# Sprint 5: Reorganización de Arquitectura y Dominios

## Objetivo
Transformar el proyecto hacia una arquitectura limpia y estandarizada, separando claramente la capa de servicios externos, unificando la nomenclatura de la base de datos y desacoplando componentes en desuso.

## Tareas Realizadas

- [x] **Desacoplamiento de la API (Stand-by)**: Se movió la carpeta `src/api/` a la raíz del proyecto (`/api`).
- [x] **Creación de la Capa de Servicios (`src/services/`)**: 
   - Se agrupó `ruc_downloader.py`.
   - Se migró `marangatu` a `services/marangatu_scraper/`.
   - Se migró `chats/chatGPT` a `services/chatgpt/`.
- [x] **Estandarización de la Base de Datos (`src/db/`)**: 
   - Se renombró `dataBase/` a `db/` y `schemas/` a `models/`.
- [x] **Refactorización de Importaciones**: Se actualizó recursivamente todo el código para que apunte a las nuevas estructuras de carpetas usando un script global de Reemplazo Regex en Python.
- [x] **Limpieza Extra**: Se eliminaron directorios y archivos de código muerto (`controllers/`, `libs/`, `scrapy/`, `file.ipynb`, `geckodriver.log`).
- [x] **Pruebas de Regresión**: La compilación pasó al 100% y los tests unitarios (`tests_main.py`) volvieron a dar **OK**.

## Estado
**Completado.** La arquitectura de carpetas ahora sigue los más altos estándares de Python y está lista para crecer de forma limpia.
