# Observaciones del Proyecto (OBSERVATIONS.md)

Este archivo actúa como un registro de descubrimientos técnicos ("quirks"), decisiones de arquitectura temporal o advertencias dejadas durante el ciclo de desarrollo para futuros desarrolladores o agentes de código.

## 1. El Problema de las Importaciones Relativas vs Absolutas
- **Tests y API unificados**: Durante el Sprint 2, se arregló el conflicto de rutas. Ahora TODO el proyecto (Bot, API y Tests) asume que `src/` es la raíz de ejecución.
- Comando unificado para la API: `cd src && python -m uvicorn api.main:app`
- Comando unificado para tests: `cd src && python -m unittest tests/tests_main.py`

## 2. Selenium, `marangatu.py` y Orquestación Docker
- Durante el **Sprint 10**, se eliminaron los `sleep()` manuales y XPath frágiles, reemplazándolos por esperas explícitas (`WebDriverWait`).
- **Capturas de Pantalla Defensivas**: Si ocurre un `TimeoutException` de Selenium, el bot ahora utiliza la función `save_error_screenshot()` para dejar un registro fotográfico del navegador antes de cerrar la sesión, facilitando el debugeo de cambios visuales en el portal gubernamental.
- **Docker Compose Quirk**: El contenedor oficial de Firefox requiere el parámetro `shm_size: '2g'` en `docker-compose.yml`. Si en algún momento se borra, Firefox "crasheará" internamente en descargas pesadas de la DNIT sin previo aviso por desbordamiento de memoria compartida.
- **VNC en Vivo**: Para observar al bot operando en tiempo real en la nube, acceder a `http://localhost:7900` (puerto expuesto en el compose).

## 3. Discos en Red y Volúmenes de Docker
- Originalmente, el proyecto estaba amarrado a `Z:/r90` y `Z:/anulados`. Ha sido parcheado con variables de entorno (`.env`). Cuando el bot se despliega usando Docker, es **obligatorio** que estos discos de red sean mapeados físicamente en la sección `volumes:` del archivo `docker-compose.yml` (e.g. `/mnt/z/r90:/app/archives/r90`) para que el SO subyacente de Linux tenga acceso a ellos.

## 4. Estructura de "file_manager"
- La función de convertir Excel a HTML del R-90 es la más completa. Es importante notar que descarga el documento localmente, llama a Pandas (vía `utils/html_convert.py`) y luego **borra** físicamente los documentos usando `os.remove` inmediatamente después de enviarlos al chat para no saturar el servidor.
