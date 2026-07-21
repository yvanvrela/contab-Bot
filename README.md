# contabBot

## Descripción

Bot de Telegram desarrollado en Python para firmas contables en Paraguay. 
Automatiza el control de vencimiento de timbrados, la descarga de listados de RUC (DNIT), el procesamiento de planillas de la R-90, la gestión de facturas anuladas y ofrece resúmenes instantáneos de archivos Excel. Cuenta con integración de Inteligencia Artificial (OpenAI) para mantener conversaciones naturales y una arquitectura segura de acceso y manejo masivo de bases de datos.

## Funciones Principales

### Búsqueda Mágica de Contribuyentes (DNIT / SET)
Gracias a la indexación de más de 2 millones de contribuyentes en la base de datos interna, Benito responde en milisegundos a las consultas del equipo:
- **Por Número:** Si simplemente envías un número de cédula (`1234567`) o un RUC (`1234567-8`) al chat, el bot responderá inmediatamente con la tarjeta del contribuyente (Nombre, RUC, Estado).
- **Por Nombre:** Puedes escribir `buscar juan perez` o `ruc de juan` y Benito escaneará la base de datos devolviendo los 5 contribuyentes que más se acerquen al nombre.
- *(También soporta el antiguo comando `/buscarci` por retrocompatibilidad).*

### Procesamiento de Archivos (Arrastrar y Soltar)
- **Generador de Resúmenes (Excel a HTML)**
  - Al enviar un archivo `.xlsx` (formato de facturación electrónica / R-90) directamente al bot, este lo procesa automáticamente.
  - Limpia el documento, calcula las bases imponibles (Monto Gravado 10% y 5%) a partir de los totales, suma todas las columnas y devuelve un archivo `.html` ligero.
  - Responde en el chat con un resumen rápido de los totales (Gravada 10%, Gravada 5%, Exenta).

### Exportación y Marangatu (SET / DNIT)
- **/downloadruc**
  - Descarga los archivos ZIP de RUCs de la página de la DNIT, los descomprime, hace una inyección masiva (*bulk insert*) a la base de datos local y elimina la "basura" en ~80 segundos.
  - El usuario puede ver el **progreso en tiempo real** en un único mensaje que el bot actualiza visualmente fase por fase.
- **/export**
  - Busca archivos XLS generados, los formatea a TXT tabulado y los empaqueta en `.zip` para la presentación de la R-90 - Marangatu.
- **/anulados**
  - Explora el disco en red buscando registros de facturas anuladas, agrupando datos por contribuyente para facilitar su baja en el sistema.

### Control y Base de Datos
- **Seguridad y Accesos (is_active)**: El bot cuenta con un middleware estricto. Registra de manera silenciosa a cada persona o grupo que interactúa con él en la base de datos `contabot.db`. Si el registro tiene el flag `is_active = False`, Benito negará los servicios y bloqueará el chat automáticamente.
- **/agregartimbrado**: Carga un nuevo timbrado a la base de datos para controlar vencimientos.

### Inteligencia Artificial y Chat Diario
- **Chat Sarcástico (OpenAI)**: Reacciona a saludos, cumplidos y regaños usando la API moderna (v1+) de ChatGPT, actuando con una personalidad sarcástica predefinida (Benito).
- **Control de Insumos**: 
  - Si se escribe "falta [insumo]", lo guarda en una lista.
  - Si se pregunta "¿qué falta?", devuelve la lista de compras pendientes.
  - Si se escribe "comprado", limpia la lista de despensa.

## Instalación y Ejecución

El proyecto soporta dos modos de ejecución: Despliegue Empresarial (Docker) y Desarrollo Local.

### Opción A: Despliegue con Docker (Recomendado)
Esta es la manera más robusta de ejecutar el robot. Al levantar la orquestación, se encenderán dos contenedores separados: uno corriendo la inteligencia de Python y el otro corriendo una versión aislada ("Headless") de Firefox.
1. Configura tus variables de entorno copiando la plantilla:
   ```bash
   cp .env.example .env
   ```
   Rellena tus tokens. La variable `SELENIUM_URL` puede quedar vacía, el orquestador la sobrescribirá automáticamente para enlazar los contenedores.
2. Inicia el ecosistema en segundo plano:
   ```bash
   docker-compose up -d
   ```
*Tip de Depuración:* El contenedor de Firefox expone un servidor VNC en vivo. Si quieres ver al bot navegar por Marangatu en pantalla, entra a `http://localhost:7900` desde cualquier navegador (Contraseña por defecto: `secret`).

### Opción B: Desarrollo Local
1. Crea y activa un entorno virtual de Python:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Linux/Mac usa: source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configura las variables copiando la plantilla:
   ```bash
   cp .env.example .env
   ```
3. Ejecuta el bot utilizando el script automatizado (desde la raíz del proyecto):
   ```bash
   bash src/run-bot.sh
   ```
   El script detectará tu sistema operativo, activará el entorno virtual y encenderá el bot con soporte de entorno gráfico local (si `SELENIUM_URL` está vacío en tu `.env`, abrirá un Firefox visible en tu PC).
