# Utilizar una imagen oficial de Python ligera
FROM python:3.11-slim

# Configurar variables de entorno para optimizar la ejecución en contenedor
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema operativo (si fueran necesarias para algunas librerías)
# Por ejemplo, para compilar ciertos paquetes o usar locales
RUN apt-get update && apt-get install -y locales \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i es_ES -c -f UTF-8 -A /usr/share/locale/locale.alias es_ES.UTF-8

# Configurar locale
ENV LANG es_ES.utf8

# Copiar el archivo de requerimientos primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente del proyecto al contenedor
COPY . .

# Comando por defecto para iniciar el bot (desde la raíz para respetar el sys.path unificado)
CMD ["python", "src/main.py"]
