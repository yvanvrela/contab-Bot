# Sprint 1: Seguridad y Configuración

## Objetivo
Securizar el entorno de desarrollo y producción eliminando credenciales expuestas y rutas de disco "hardcodeadas" en el código fuente.

## Tareas Realizadas
- [x] Crear archivo `.env` y plantilla `.env.example`.
- [x] Extraer `TOKEN` de Telegram y `OPENAI_TOKEN` del archivo `run-bot.sh` e integrarlos al `.env`.
- [x] Refactorizar llamadas de variables de entorno de `os.environ['KEY']` a `os.environ.get('KEY')` mediante `python-dotenv`.
- [x] Reemplazar rutas quemadas de discos en red (`Z:/r90` y `Z:/anulados`) por variables parametrizables (`PATH_R90` y `PATH_ANULADOS`).
- [x] Agregar el `.env` al `.gitignore` para proteger las llaves.
- [x] Reescribir `run-bot.sh` para funcionar únicamente como un script lanzador inteligente (auto-detección de SO y virtualenv).

## Estado
**Completado.** El código base ya no expone llaves críticas a repositorios públicos y es capaz de ejecutarse en diferentes computadoras sin depender de discos predefinidos.
