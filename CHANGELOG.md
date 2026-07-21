# Changelog
Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [Unreleased]

### Agregado
- Archivo de planificación `sprint-13-busqueda-secuencial.md` documentando la próxima optimización del motor de búsqueda (cortocircuito) y el blindaje contra *Timeouts* de la API del MEC.
- **Orquestación (Sprint 12.3)**:
  - Se creó el archivo `docker-compose.yml` dividiendo la arquitectura en servicios de micro-contenedores.
  - El bot de Python ahora convive con un contenedor satélite oficial de Selenium (`selenium/standalone-firefox`) en una red virtual interna, logrando que el entorno sea "Headless" y altamente portable.
  - Se habilitó la persistencia mediante volúmenes de Docker para evitar que SQLite se borre con los reinicios de contenedor.
- Archivo de planificación `sprint-12.3-orquestacion.md` con las directrices para conectar el Bot y el contenedor de Selenium mediante `docker-compose.yml`.
- **Contenedores (Sprint 12.2)**: 
  - Se crearon los archivos base para Docker: `Dockerfile` (optimizado con Python 3.11-slim y generación de locales en español) y `.dockerignore` para mantener la imagen ligera.
- Archivo de planificación `sprint-12.2-dockerfile.md` con las instrucciones detalladas para empaquetar el entorno Python y optimizar las capas de caché de Docker.
- **Adaptación Docker (Sprint 12.1)**:
  - Se modificó la inicialización del scraper de Marangatu (`webdriver`) para soportar ejecución dentro de contenedores (`webdriver.Remote`).
  - Se añadió la variable `SELENIUM_URL` al entorno (`.env` y `.env.example`). Si la variable está presente, el bot se conectará a un nodo remoto de Firefox; si no, funcionará como siempre abriendo Firefox de forma local.
- Planificación del **Sprint 12 (Dockerización)** estructurada en sub-fases dentro de `sprints/sprint-12/`.
- Archivo de planificación `sprint-11-migracion-asincrona.md` detallando los pasos para escalar la librería de Telegram a la versión 20+ (soporte multitarea).
- Archivo de planificación `sprint-10-estabilizar-selenium.md` para la futura refactorización y blindaje de las rutinas de automatización web (Marangatu).
- **Búsqueda Mágica (Sprint 8)**:
  - El bot ahora detecta automáticamente si se envía un número suelto (Ej: `123456` o `123456-7`) al grupo y responde inmediatamente con los datos fiscales de esa persona. No hace falta usar el comando `/buscarci`.
  - El bot ahora acepta búsquedas por nombre escribiendo `buscar [nombre]` o `ruc [nombre]`. Buscará en la base de datos de 2 millones de personas usando el operador `LIKE` y devolverá los 5 resultados más cercanos, siempre formateados en MAYÚSCULAS.
- Archivo de planificación `sprint-7-optimizacion-bd-rucs.md` para migrar y optimizar el guardado y consulta de datos del DNIT (RUCs) en memoria hacia SQLite.
- Plantilla `.env.example` para documentar requerimientos de entorno.
- Archivo de planificación `sprint-6-migracion-usuarios-bd.md` para migrar listas de chats en `.txt` hacia SQLite.
- Carpeta `src/sprints/` para documentar la planificación del desarrollo.
- Archivos de control `CHANGELOG.md` y `OBSERVATIONS.md` en `src/`.
- Archivo `src/docs/architecture.md` con un diagrama Mermaid detallando los componentes.

### Arreglado
- **Correcciones post-migración Asíncrona**:
  - Se solucionó un error crítico de concurrencia (`This session is in 'prepared' state`) que provocaba que Benito se congelara por completo al intentar realizar la descarga masiva de RUCs (`/downloadruc`) mientras otros usuarios enviaban mensajes. Se migró la base de datos a `scoped_session` (Sesiones de Hilo Aisladas) para permitir paralelismo real sin corromper SQLAlchemy.
  - Se arregló un bug crítico (`KeyError: 'names'`) en el formateador de HTML (`html_convert.py`) introducido durante la optimización de SQLite del Sprint 7. El bot ahora genera correctamente el nombre del archivo final basándose en el campo unificado `fullname`.
  - Se actualizaron las rutas de importación obsoletas de Telegram v13 (`ParseMode` movido a `telegram.constants`).
  - Se solucionó un error de colisión de zonas horarias al inicializar la aplicación. Se forzó la actualización de `APScheduler` a la versión `3.11.3` para dar soporte a objetos de tiempo nativos (`zoneinfo`) de Python 3.11+, permitiendo que el Cron Job interno inicie correctamente sin depender de `pytz`.

### Cambiado
- **Arquitectura de Búsqueda (Sprint 13)**:
  - Se optimizó drásticamente el buscador de identidad: el bot ahora emplea "Cortocircuito Lógico" y solo acude a Internet (Web del MEC) si no logra encontrar a la persona en la ultrarrápida base de datos local (SQLite).
  - Se agregó una protección de *Timeout (5s)* a las peticiones del MEC, evitando que fallas o caídas de los servidores gubernamentales congelen los procesos del bot indefinidamente.
  - La URL de búsqueda de la API gubernamental ahora está parametrizada dinámicamente en el `.env`.
- **Arquitectura Asíncrona (Sprint 11)**:
  - Se completó exitosamente la migración del framework `python-telegram-bot` desde su versión heredada `13.14` hacia la versión moderna `v20+`.
  - El bot abandonó el modelo de bloqueo síncrono. Ahora es un bot verdaderamente asíncrono (`async/await`) capaz de atender a decenas de usuarios en paralelo.
  - Se refactorizó la totalidad de los Handlers (`src/handlers/`) para soportar corrutinas.
  - Todas las operaciones pesadas de base de datos (`SQLite`), procesamiento de tablas (`Pandas`) y descargas web se aislaron de manera segura usando `asyncio.to_thread` para que nunca congelen el hilo principal de la aplicación.
- **Automatización Marangatu (Sprint 10)**:
  - Se eliminaron por completo las peligrosas esperas fijas (`sleep()`) en el scraper de Selenium, reemplazándolas por "Esperas Explícitas" (`WebDriverWait`).
  - Se refactorizaron las fragiles rutas absolutas (`XPath`) cambiándolas por selectores relativos inteligentes, evitando que el bot se rompa con pequeñas actualizaciones estéticas de la web gubernamental.
  - Se agregó soporte visual de errores: Si la web no carga, el bot saca una "captura de pantalla" (`.png`) del navegador invisible para ayudar al programador a saber qué falló antes de cerrarse.
- **Manejo de Basura y Temporales (Sprint 9)**:
  - Se solucionó el bug donde los archivos Excel y HTML procesados por Benito quedaban permanentemente "huérfanos" en la raíz del proyecto si ocurría un error durante el parseo de datos.
  - Se creó un directorio dedicado protegido por Git (`src/temp/`) para procesar descargas.
  - Se blindó la función `file_manager` con un patrón defensivo `try...finally`, garantizando matemáticamente que los archivos temporales se borren del disco, incluso si la red se corta o el archivo Excel del usuario está corrupto.
- **UX y Feedback Visual (Comando /downloadruc)**:
  - Se modificó la interfaz del comando de actualización de bases de datos de RUCs.
  - El bot ahora edita un único mensaje en vivo ("mensaje vivo") para reportar en qué estado de descarga se encuentra (1 de 10... 5 de 10...), evitando que el usuario piense que el sistema se colgó durante los 90 segundos que demora en procesar los 2 millones de registros.
- **Optimización Extrema de Datos (Sprint 7)**:
  - Se rediseñó el proceso completo de descarga y consulta de RUCs de la SET (`/downloadruc`).
  - La base de datos local SQLite ahora ingesta cerca de 2 millones de contribuyentes utilizando inserciones masivas (`bulk_insert`) en tiempo récord (~80 segundos en total para procesar 120MB de datos).
  - Los archivos `.txt` y `.zip` residuales del DNIT se eliminan del disco automáticamente después de la inyección en base de datos.
  - Las búsquedas (`/buscarci` o por procesamiento de planillas R-90) pasaron de usar fuerza bruta en archivos de texto, a utilizar índices relacionales (`index=True`) de la BD, **reduciendo el tiempo de búsqueda a 0.008 segundos por contribuyente**.
- **Autorización (Sprint 6)**:
  - Se eliminaron los archivos físicos `archives/chats/users.txt` y `groups.txt`.
  - La lógica de acceso del bot ahora se maneja 100% mediante las tablas `users` y `groups` en SQLite (`contabot.db`), habilitando las columnas de control de estado (`is_active`).
  - Se creó un middleware interceptor (`auth_handler.py`) configurado en el grupo `-1` del Dispatcher. Ningún mensaje es procesado si el grupo o el usuario están desactivados en la base de datos.
- **Arquitectura de Dominios (Sprint 5)**:
  - Se movió la aplicación `api/` a la raíz del proyecto para desacoplarla de la ejecución core del Bot (dado que usan bases de datos diferentes).
  - Se estandarizó la nomenclatura de bases de datos: `dataBase` pasó a ser `db/` y sus `schemas/` pasaron a ser `models/`.
  - Se agruparon todas las integraciones de internet bajo la nueva carpeta `src/services/` (Marangatu, ChatGPT, RUC Downloader).
  - Se eliminaron carpetas huérfanas y código muerto (`controllers/`, `libs/`, `scrapy/`, `file.ipynb`).
- **Refactorización Core (Sprint 4)**:
  - El monolito `src/main.py` de ~500 líneas fue completamente desacoplado y reducido a ~70 líneas de orquestación.
  - Se creó la carpeta `src/handlers/` separando la lógica en `base_handlers`, `chat_handlers`, `file_handlers`, `r90_handlers`, `ruc_handlers` y `timbrado_handlers`.
  - Se creó la carpeta `src/jobs/` extrayendo las tareas cronometradas (`saludo`, `search_timbrados_to_expire`).
  - Se actualizó el diagrama de arquitectura en `src/docs/architecture.md` para reflejar el nuevo orquestador y los controladores.
- **Modernización y Dependencias (Sprint 3)**:
  - Se purgó el archivo `requirements.txt`, pasando de 98 dependencias a tan solo 13 dependencias estrictamente necesarias para el bot y la API.
  - Se actualizó el código de IA (`chatGPT_chat.py`) para ser 100% compatible con la nueva arquitectura de **OpenAI v1+**.
- **Refactorización (Sprint 2)**:
  - Se eliminaron los bloques `except:` vacíos (bare excepts) en el web scraper de `marangatu.py`, reemplazándolos por `except Exception as e:` y enviando el error al log para no ocultar bugs.
  - Se implementó la librería estándar `logging` en `tests_main.py`, `html_convert.py`, `create_archives.py` y `document_util.py` para reemplazar llamadas inseguras de `print()`.
  - Se unificó el sistema de importaciones. Ahora tanto la API (`src/api`), los Tests y el Bot principal asumen unánimemente la carpeta `src/` como raíz de ejecución, resolviendo el problema documentado en Observaciones.
- **Seguridad**: Se eliminaron los tokens y secretos (`TOKEN`, `OPENAI_TOKEN`) del script en bash `run-bot.sh` y se migraron a `.env`.
- Archivo `run-bot.sh` refactorizado para detectar el SO y activar virtualenv correctamente.
- Módulos `marangatu.py`, `export_files.py` y `create_archives.py` ahora usan `python-dotenv` para cargar rutas (`Z:/r90`, `Z:/anulados`).
- Documentación principal `README.md` y `AGENTS.md` actualizados para reflejar funciones reales y contextos de ejecución.

### Eliminado
- Instrucciones desactualizadas en `README.md` referentes a comandos inactivos (ej. `/nuevocliente`, `/colorcarpeta`).
