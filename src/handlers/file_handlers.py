import os
import asyncio
import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from utils.html_convert import to_html
from utils.constants import TaxAuthority

logger = logging.getLogger(__name__)

async def file_manager(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    
    # Directorio temporal seguro
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    temp_dir = os.path.join(basedir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    file_download = None
    html_path = None

    try:
        # Download file
        document = update.message.document
        file_id = document.file_id
        file_name = document.file_name or 'archivo.xlsx'
        
        file_download = os.path.join(temp_dir, file_name)
        
        telegram_file = await context.bot.get_file(file_id)
        await telegram_file.download_to_drive(custom_path=file_download)
        
        await update.message.reply_text("⏳ Procesando planilla, por favor espera...", disable_notification=True)

        # Format file
        result_data = await asyncio.to_thread(to_html, path_xlsx=file_download, out_dir=temp_dir)
        html_path = result_data['path_html']

        # Send HTML Document
        with open(html_path, 'rb') as doc_file:
            await context.bot.send_document(chat_id=chat_id, document=doc_file)

        # Send resumen data
        msg_resume = f'📊 *Resumen*\n_{result_data["file_name"]}_\n\n*Grav 10:* `{result_data["total_grav_10"]}`\n*Grav 5:* `{result_data["total_grav_5"]}`\n*Exenta:* `{result_data["total_exenta"]}`'
        await context.bot.send_message(chat_id=chat_id, text=msg_resume, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        logger.error(f"Error procesando archivo Excel en file_manager: {e}")
        await context.bot.send_message(
            chat_id=chat_id, 
            text=f"❌ Ocurrió un error al procesar tu planilla. Asegúrate de que sea un archivo de la {TaxAuthority.NAME.value} válido."
        )

    finally:
        # Garantía matemática de borrado (Limpieza de basura)
        if file_download and os.path.exists(file_download):
            try:
                os.remove(file_download)
            except OSError as e:
                logger.warning(f"No se pudo borrar el archivo temporal Excel: {e}")
                
        if html_path and os.path.exists(html_path):
            try:
                os.remove(html_path)
            except OSError as e:
                logger.warning(f"No se pudo borrar el archivo temporal HTML: {e}")
