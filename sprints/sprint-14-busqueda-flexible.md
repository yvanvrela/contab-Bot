# Sprint 14: Flexibilidad de Búsqueda y Acentos

## Objetivo
Mejorar el motor de búsqueda por nombres para que ignore el orden de las palabras y los acentos diacríticos (sin afectar a la 'Ñ'), e independizar las palabras activadoras del bot hacia variables de entorno.

## Tareas Realizadas

- [x] **Palabras Clave Configurables desde `.env`**
   - Se añadió la variable `SMART_SEARCH_KEYWORDS` a los archivos de entorno.
   - El enrutador `main.py` y el controlador `ruc_handlers.py` leen esta lista, la separan, la ordenan por longitud descendente (para evitar colisiones lógicas como "ruc de" vs "ruc") y generan un `Regex` dinámico en tiempo de ejecución.

- [x] **Ignorar Acentos (Input Inteligente)**
   - Se creó la función `remove_accents_preserve_n` en el repositorio de la base de datos que sustituye vocales con tildes pero protege culturalmente la letra `Ñ`.
   - Se utiliza la función nativa `func.replace` de SQLAlchemy para igualar las condiciones dentro de SQLite, haciendo que el usuario pueda escribir con o sin acento, y en mayúscula o minúscula.

- [x] **Búsqueda Flexible (Sin importar el orden)**
   - Se separó el *query* del usuario por palabras individuales.
   - Se inyectó el operador lógico `and_()` construyendo condiciones `LIKE` separadas.
   - Ahora, buscar "Gomez Maria" encontrará exactamente a "MARIA GOMEZ", permitiendo encontrar empresas o contribuyentes incluso si están registrados con los apellidos invertidos.

## Estado
**Completado.** La Inteligencia de búsqueda es ahora robusta, veloz y sumamente amigable para el usuario final.
