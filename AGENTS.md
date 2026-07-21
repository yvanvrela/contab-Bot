# AGENTS.md

## Overview
**contabBot** is a Telegram bot for Paraguayan businesses. It handles document receipt, stamp control, physical folder organization, and R-90 data export (Marangatu / DNIT).

## Core Quirks & Execution
- **Run the Bot (Docker)**: Use `docker-compose up -d`. This orchestrates the Python app and an isolated Selenium (Firefox) container. The bot will automatically inject `SELENIUM_URL` to connect to it.
- **Run the Bot (Local)**: `bash src/run-bot.sh` (This launcher auto-detects OS, activates `venv`, and ensures `src/` is the working directory).
- **Environment Variables**: The project strictly requires a `.env` file at the root. Do NOT hardcode secrets. Network drives (e.g., `Z:/anulados`) must be configured via `.env` paths (`PATH_R90`, `PATH_ANULADOS`).
- **Tests require `src/` context**: Do NOT run tests from the project root. The test files use imports assuming `src/` is the root module.
  - **Correct test command**: `cd src && python -m unittest discover tests/`
- **Authorization Interceptor**: Any new handler added to `main.py` is automatically protected by `auth_handler.py` (Dispatcher Group `-1`). Users/Groups are auto-registered in SQLite but MUST have `is_active=True` manually set to interact with the bot.

## Architectural Constraints
- **Asynchronous Execution (`python-telegram-bot>=20.0`)**: 
  - All handlers and scheduled jobs must be `async def`.
  - **CRITICAL**: All blocking operations (SQLAlchemy queries, Selenium scraping, Pandas file processing) MUST be wrapped in `await asyncio.to_thread(...)` to avoid freezing the Telegram event loop.
- **Selenium (Marangatu Scraper)**: 
  - Do NOT use `sleep()`. Always use explicit waits (`WebDriverWait`).
  - Use `self.save_error_screenshot()` in `except Exception` blocks to capture DOM state on failure.
  - Selenium tests in `tests_marangatu.py` use `unittest.mock` (Mocking `WebDriverWait` and `Firefox`) so they can run without a real browser or credentials.
- **File Management**: 
  - Always use `src/temp/` for processing user uploads.
  - You MUST wrap file operations in `try...finally` with `os.remove()` in the `finally` block to guarantee garbage collection.

## Project Structure
- **`src/main.py`**: Telegram bot entrypoint (`ApplicationBuilder`). Maps routes.
- **`src/handlers/` & `src/jobs/`**: Telegram commands and cron tasks.
- **`src/db/`**: SQLAlchemy ORM (SQLite `contabot.db`).
- **`src/services/`**: External integrations (Marangatu Scraper, OpenAI v1+, DNIT/RUCs).
- **`api/`**: FastAPI backend (Parked at root, decoupled from bot).

## Verification
- **Database Inspection**: `sqlite3 src/db/config/contabot.db .schema`
- **RUC Searches**: There are ~2 million taxpayers. Always query `ContribuyenteModel` in SQLite (it is indexed). Do NOT read raw text files.