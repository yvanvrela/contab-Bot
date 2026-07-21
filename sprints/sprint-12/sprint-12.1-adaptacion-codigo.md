# Sprint 12.1: Adaptación de Selenium a Entorno Remoto

## Objetivo
Preparar el código del bot de Marangatu para que sea capaz de ejecutarse dentro de un contenedor Docker sin interfaz gráfica, conectándose a un navegador aislado a través de la red.

## Tareas Realizadas

- [x] **Añadir Variable de Entorno (`.env`)**
   - Se incorporó la variable `SELENIUM_URL` comentada por defecto en `.env` y `.env.example`.

- [x] **Refactorizar la Inicialización (`MarangatuBot`)**
   - Se actualizó el constructor de `MarangatuBot` en `src/services/marangatu_scraper/marangatu.py`.
   - El código ahora lee `os.environ.get('SELENIUM_URL')`. Si encuentra una dirección, instanciará `webdriver.Remote`. Si la variable está vacía, hará *fallback* al comportamiento clásico e instanciará `webdriver.Firefox()` de manera local.

## Estado
**Completado.** El código base ya es oficialmente "Docker-ready". Puede ejecutarse tanto en tu PC sin configuraciones extra como dentro de un clúster de servidores aislados.
