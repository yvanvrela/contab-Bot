import os
import locale
import logging
from dotenv import load_dotenv

# Load env variables FIRST
load_dotenv()

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler

# Import handlers
from handlers.auth_handler import check_authorization
from handlers.base_handlers import start, help_command, done
from handlers.chat_handlers import echo
from handlers.ruc_handlers import search_identity, identity, run_download_ruc, instant_search_number, instant_search_name, IDENTITY
from handlers.timbrado_handlers import wait_timbrado, timbrado, TIMBRADO
from handlers.r90_handlers import export_files_r90, export_anulados
from handlers.file_handlers import file_manager

# Import jobs
from jobs.scheduled_tasks import saludo, search_timbrados_to_expire

# Iniciar Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN', '')

def main():
    """Inicia el bot con un TOKEN"""
    app = ApplicationBuilder().token(TOKEN).build()

    # Tiempo local, español
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
    except locale.Error:
        logger.warning("Locale 'es_ES.utf8' no está disponible en este sistema.")

    # obtener el job_queue del updater
    # job = app.job_queue
    # job.run_once(search_timbrados_to_expire, 1)

    dp = app

    # Authorization Check (Group -1 runs before Group 0)
    dp.add_handler(MessageHandler(filters.ALL, check_authorization), group=-1)

    # Conversaciones
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("buscarci", search_identity)],
        states={
            IDENTITY: [MessageHandler(filters.Regex("^[\d,-]*$"), identity)],
        },
        fallbacks=[MessageHandler(filters.Regex("(?i)^listo$"), done)],
    )

    conv_handler_timbrado = ConversationHandler(
        entry_points=[CommandHandler("agregartimbrado", wait_timbrado)],
        states={
            TIMBRADO: [MessageHandler(filters.Regex("\w"), timbrado)],
        },
        fallbacks=[MessageHandler(filters.Regex("(?i)^listo$"), done)],
    )

    dp.add_handler(conv_handler)
    dp.add_handler(conv_handler_timbrado)

    # File manager filter
    dp.add_handler(MessageHandler(filters.Document.ALL, file_manager))

    # Comandos básicos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ayuda', help_command))
    
    # Comandos R90 y Marangatu
    dp.add_handler(CommandHandler('export', export_files_r90))
    dp.add_handler(CommandHandler('anulados', export_anulados))
    dp.add_handler(CommandHandler('downloadruc', run_download_ruc))

    # Búsqueda Mágica por Número o Nombre (Evita usar el comando /buscarci)
    dp.add_handler(MessageHandler(filters.Regex(r"^\d{4,9}(?:-\d)?$"), instant_search_number))
    dp.add_handler(MessageHandler(filters.Regex(r"(?i)^(?:buscar|ruc(?: de)?)\s+(.+)"), instant_search_name))

    # Echo handling (Inteligencia Artificial, Lista de súper, Respuestas predeterminadas)
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot iniciado correctamente. Esperando mensajes...")
    # Start the Bot
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
