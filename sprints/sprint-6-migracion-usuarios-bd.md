# Sprint 6: Migración de Acceso y Autorización a Base de Datos

## Objetivo
Migrar el sistema de guardado de usuarios y grupos de archivos de texto plano (`.txt`) a la base de datos relacional SQLite (`contabot.db`), habilitando un sistema de autorización basado en el estado (activo/inactivo).

## Estructura de Datos Propuesta

### Modelo `Users` (Usuarios)
- `telegram_id` *(Integer, Unique)*: ID inmutable de Telegram.
- `username` *(String)*: Alias en Telegram (ej. `@juanperez`).
- `first_name` *(String)*: Nombre público.
- `last_name` *(String)*: Apellido público.
- `is_bot` *(Boolean)*: Indica si es otro bot.
- `is_active` *(Boolean, Default: True)*: Bandera de autorización para interactuar con Benito.
- `created_at` *(DateTime)*: Fecha de primer uso.

### Modelo `Groups` (Grupos)
- `telegram_id` *(Integer, Unique)*: ID del grupo (usualmente negativo).
- `title` *(String)*: Nombre del grupo.
- `type` *(String)*: Tipo de grupo (`group` o `supergroup`).
- `is_active` *(Boolean, Default: True)*: Bandera de autorización para que Benito responda en dicho grupo.
- `created_at` *(DateTime)*: Fecha de primer registro.

## Tareas Realizadas
- [x] **Actualizar Modelos SQLAlchemy**: Reemplazar `UsersModel` en `src/db/config/config_db.py` y crear el nuevo `GroupsModel`.
- [x] **Migrar la Base de Datos**: Como se usan modelos nuevos, se borró la tabla `users` vieja y vacía de `contabot.db` usando sentencias puras de SQLite para que SQLAlchemy construyera la nueva versión.
- [x] **Crear Repositorios (CRUD)**: Desarrollar `users_repository.py` y `groups_repository.py` dentro de `src/db/repositories/`.
- [x] **Refactorizar `office_require.py`**: Eliminar la lógica de lectura/escritura de `archives/chats/*.txt` y conectar las funciones a los repositorios de la BD.
- [x] **Implementar Filtro de Acceso**: Se inyectó un `auth_handler` ejecutándose en el `group=-1` del dispatcher (interceptor primario) que chequea `is_active`.
- [x] **Limpieza**: Borrar los viejos archivos de texto `archives/chats/users.txt` y `groups.txt`.

## Estado
**Completado.** El sistema ahora cuenta con un nivel de administración y control de acceso robusto basado en BD.
