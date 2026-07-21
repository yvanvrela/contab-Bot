# Sprint 10: Estabilización del Scraper de Marangatu (Selenium)

## Objetivo
Refactorizar la lógica de automatización web (`src/services/marangatu_scraper/marangatu.py`) para hacerla resistente a problemas de latencia de red y a cambios en la interfaz gráfica de la página de la SET/DNIT, abandonando el uso frágil de `sleep()` y `XPath` absolutos.

## Análisis del Problema
Actualmente, el bot de Selenium navega por el portal Marangatu utilizando temporizadores fijos (ej. `sleep(3)`) y rutas XPath absolutas extremadamente largas (ej. `/html/body/div[1]/div/div[2]/div/...`).
1. **Problema de Latencia:** Si el servidor de la DNIT tarda 4 segundos en cargar en lugar de 3, el bot fallará porque buscará un botón que aún no existe.
2. **Fragilidad de la Interfaz:** Si el administrador de la página añade un simple menú extra o mueve una tabla un píxel, la ruta XPath cambiará y romperá la ejecución por completo.

## Tareas Realizadas

- [x] **Reemplazar `sleep()` por Esperas Explícitas (WebDriverWait)**
   - Se reemplazaron todas las sentencias `sleep(n)` por `self.wait.until(EC...)`, reduciendo masivamente el tiempo de ejecución y protegiendo contra latencia de red.
- [x] **Reemplazar XPath absolutos por Localizadores Robustos**
   - Se cambiaron las rutas estáticas por rutas XPath relativas combinadas (ej. `//a[contains(text(), 'Presentación')] | /html/body/div...`), garantizando compatibilidad hacia atrás mientras se navega de forma robusta.
- [x] **Manejo de Errores (Screenshots de Fallo)**
   - Se agregó `self.save_error_screenshot()` dentro de bloques `try...except Exception` a lo largo de toda la clase.
- [x] **Creación de Tests Automatizados (`src/tests/test_marangatu.py`)**
   - Se implementaron 4 pruebas unitarias mockeando `WebDriverWait` y `webdriver.Firefox` para validar la lógica del script sin conectarse físicamente a la SET/DNIT. Las pruebas devuelven **OK**.

## Estado
**Completado.** El componente de Selenium es ahora resistente a caídas de red y cambios visuales del portal del gobierno.
