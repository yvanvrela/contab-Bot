import datetime
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ConversationHandler
from db.config.config_db import session
from db.repositories.timbrados_repository import TimbradosRepository
from db.models.timbrados_schema import TimbradoSchema

TIMBRADO = 1

async def wait_timbrado(update: Update, context):
    user = update.effective_user
    msg = 'Enviame los datos del timbrado separados por "*,*" de esta forma:\n\nCliente, N° timbrado, expedición, N° factura desde, hasta, Fecha de vencimiento'
    await context.bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.MARKDOWN)

    msg = 'Ejemplo:\n\n`Juan, 14152275, 001-001, 100, 300, 31/12/2023`'
    await context.bot.send_message(chat_id=user.id, text=msg, parse_mode=ParseMode.MARKDOWN)

    return TIMBRADO

async def timbrado(update: Update, context):
    timbrado_data_text = update.message.text.split(',')
    timbrado_data_text = [data.strip() for data in timbrado_data_text]

    inicio = timbrado_data_text[2]+'-'+timbrado_data_text[3]
    fin = timbrado_data_text[2]+'-'+timbrado_data_text[4]

    timbrado_data = TimbradoSchema(
        client_name=timbrado_data_text[0],
        timbrado_number=timbrado_data_text[1],
        numero_inicio=inicio,
        numero_fin=fin,
        end_date=datetime.datetime.strptime(timbrado_data_text[5], '%d/%m/%Y')
    )
    insert_db = await asyncio.to_thread(TimbradosRepository(session).add_timbrado, timbrado_data)
    if insert_db:
        await update.message.reply_text('Timbrado agregado')
    else:
        await update.message.reply_text('No pude agregarlo, intenta de nuevo')

    return ConversationHandler.END
