import asyncio
from telegram import Update
from telegram.ext import CallbackContext, ApplicationHandlerStop
from db.config.config_db import session
from db.repositories.users_repository import UsersRepository
from db.repositories.groups_repository import GroupsRepository
from utils import office_require

async def check_authorization(update: Update, context: CallbackContext):
    """
    Se ejecuta antes de cualquier otro comando (en el grupo -1 del dispatcher).
    Verifica si el usuario y el grupo están autorizados (is_active = True).
    Además, aprovecha para registrarlos o actualizar su información.
    """
    if not update.message:
        return

    user = update.message.from_user
    chat = update.message.chat

    # Registra o actualiza la info silenciosamente
    await asyncio.to_thread(office_require.add_chat_info, update.message, user)

    # Verificar Usuario
    users_repo = UsersRepository(session)
    user_db = await asyncio.to_thread(users_repo.get_by_telegram_id, user.id)
    if user_db and not user_db.is_active:
        await update.message.reply_text("Lo siento, no tienes autorización para hablarme. Habla con un administrador.")
        raise ApplicationHandlerStop()

    # Verificar Grupo
    if chat.type in ['group', 'supergroup']:
        groups_repo = GroupsRepository(session)
        group_db = await asyncio.to_thread(groups_repo.get_by_telegram_id, chat.id)
        if group_db and not group_db.is_active:
            await update.message.reply_text("Este grupo no está autorizado para usar mis servicios.")
            raise ApplicationHandlerStop()
