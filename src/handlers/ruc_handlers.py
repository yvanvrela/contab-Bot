from telegram import Update
from telegram.constants import ParseMode
import os
import re
import asyncio
from services.ruc_downloader import download_zips, unzipping_files, scan_files as scan_zip_files
from utils.search_identity import find_identity_data
from db.config.config_db import session
from db.repositories.contribuyentes_repository import ContribuyentesRepository

IDENTITY = 1

async def instant_search_number(update: Update, context):
    """Búsqueda automática al detectar un número de CI o RUC suelto en el chat"""
    identity_number = update.message.text.strip()
    message_person_data = await asyncio.to_thread(find_identity_data, identity_number)
    await update.message.reply_text(message_person_data, parse_mode=ParseMode.MARKDOWN)

async def instant_search_name(update: Update, context):
    """Búsqueda mágica por nombre parametrizada"""
    text = update.message.text.strip()
    
    # Extraer el nombre de la consulta (ej. "buscar juan perez" -> "juan perez")
    MAGIC_SEARCH_KEYWORDS = os.environ.get('MAGIC_SEARCH_KEYWORDS', 'buscar,ruc')
    palabras = [k.strip() for k in MAGIC_SEARCH_KEYWORDS.split(',')]
    palabras.sort(key=len, reverse=True) # Ordenar por longitud descendente para atrapar 'ruc de' antes que 'ruc'
    keywords_pattern = "|".join(palabras)
    match = re.match(rf"(?i)^(?:{keywords_pattern})\s+(.+)", text)
    if not match:
        return
        
    name_query = match.group(1).strip()
    await update.message.reply_text(f"Buscando a `{name_query.upper()}`... 🔍", parse_mode=ParseMode.MARKDOWN)
    
    repo = ContribuyentesRepository(session)
    results = await asyncio.to_thread(repo.search_by_name, name_query, limit=5)
    
    if not results:
        await update.message.reply_text(f"No encontré a nadie llamado `{name_query.upper()}`.", parse_mode=ParseMode.MARKDOWN)
        return
        
    response = f"*Resultados para {name_query.upper()}:*\n\n"
    for r in results:
        # Forzar todo a mayúsculas
        fullname = str(r.fullname).upper() if r.fullname else "SIN NOMBRE"
        status = str(r.status).upper() if r.status else "DESCONOCIDO"
        ruc = str(r.ruc).upper() if r.ruc else "SIN RUC"
        
        response += f"👤 *{fullname}*\n"
        response += f"RUC: `{ruc}`\n"
        response += f"Estado: `{status}`\n"
        response += "----------------------\n"
        
    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

async def search_identity(update: Update, context) -> int:
    msg = 'Envía `Listo` cuando termines las consultas.\n\nNúmero de documento:'
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    return IDENTITY

async def identity(update: Update, context):
    identity_number = update.message.text
    message_person_data = await asyncio.to_thread(find_identity_data, identity_number)
    await update.message.reply_text(message_person_data, parse_mode=ParseMode.MARKDOWN)

async def run_download_ruc(update: Update, context):
    chat_id = update.message.chat_id
    
    # Enviar el primer mensaje vivo
    status_message = await update.message.reply_text("Iniciando actualización de la base de datos... ⏳")
    
    # Variable para guardar el texto anterior y evitar editar con el mismo texto (Telegram da error)
    last_text = ""
    
    loop = asyncio.get_running_loop()

    async def update_progress(text: str):
        nonlocal last_text
        if text != last_text:
            try:
                await context.bot.edit_message_text(chat_id=chat_id, message_id=status_message.message_id, text=text, parse_mode=ParseMode.MARKDOWN)
                last_text = text
            except Exception as e:
                pass # Ignorar si Telegram falla por editar demasiado rápido

    def sync_progress(text: str):
        # Fire and forget the coroutine into the main event loop
        asyncio.run_coroutine_threadsafe(update_progress(text), loop)

    # Pasar el callback a las funciones pesadas
    await asyncio.to_thread(download_zips, progress_callback=sync_progress)

    files = await asyncio.to_thread(scan_zip_files, '.zip')
    if files is not None:
        await asyncio.to_thread(unzipping_files, progress_callback=sync_progress)

    await update_progress("✅ *¡Base de datos actualizada con éxito!*\nMillones de contribuyentes listos y basura eliminada.")
