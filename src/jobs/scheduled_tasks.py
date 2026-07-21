import os
import datetime
import asyncio
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from services.chatgpt.chatGPT_chat import bot_response
from db.config.config_db import session
from db.repositories.timbrados_repository import TimbradosRepository

def get_group_id():
    return os.environ.get('GROUP_ID', '')

async def saludo(context: CallbackContext) -> None:
    GROUP_ID = get_group_id()
    fecha_actual = datetime.date.today()
    day = fecha_actual.strftime('%A')
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().min
    date = datetime.datetime.now().date()
    if hour >= 6 and hour <= 12:
        message = await asyncio.to_thread(
            bot_response,
            prompt=f'Te encendieron: {date}, {day} a las: {hour}:{minute}. Te encuentras en el grupo Contasaurios con los demas miembros de la empresa, no te presentes ya te conocen. Segun la hora que te encendieron Sí es menos de la 8:00hs quejate y si te encendieron despues de las 9:00hs haz un comentario de que te despertaste tarde. Saluda a todos agrega un comentario random.', 
            temperature=0.8
        )
        if message:
            await context.bot.send_message(chat_id=GROUP_ID, text=message)

async def search_timbrados_to_expire(context: CallbackContext) -> None:
    GROUP_ID = get_group_id()
    date_now = datetime.date.today()
    current_year = date_now.year
    current_month = date_now.month

    next_month = current_month + 1
    if next_month == 13:
        next_month = 1
        next_year = current_year + 1
        timbrados_to_expire_next_month = await asyncio.to_thread(TimbradosRepository(session).get_timbrado_by_date, month=next_month, year=next_year)
    else:
        timbrados_to_expire_next_month = await asyncio.to_thread(TimbradosRepository(session).get_timbrado_by_date, month=next_month, year=current_year)

    timbrados_to_expire_current_month = await asyncio.to_thread(TimbradosRepository(session).get_timbrado_by_date, month=current_month, year=current_year)

    await context.bot.send_message(chat_id=GROUP_ID, text='Buen día 🥴')

    if len(timbrados_to_expire_current_month) > 0:
        timbrados_information = [
            f'Contribuyente: `{timbrado.client_name}`\nTimbrado: `{timbrado.timbrado_number}`\nN° Ini: `{timbrado.numero_inicio}`\nN° Fin: `{timbrado.numero_fin}`\nVencimiento: `{timbrado.end_date.strftime("%d/%m/%Y")}`\n'
            for timbrado in timbrados_to_expire_current_month
        ]
        message_timbrados_expire_current = '*Timbrados a vencer este mes*\n\n' + '\n'.join(timbrados_information)
        await context.bot.send_message(chat_id=GROUP_ID, text=message_timbrados_expire_current, parse_mode=ParseMode.MARKDOWN)

    if len(timbrados_to_expire_next_month) > 0:
        timbrados_information_next = [
            f'Contribuyente: `{timbrado.client_name}`\nTimbrado: `{timbrado.timbrado_number}`\nN° Ini: `{timbrado.numero_inicio}`\nN° Fin: `{timbrado.numero_fin}`\nVencimiento: `{timbrado.end_date.strftime("%d/%m/%Y")}`\n'
            for timbrado in timbrados_to_expire_next_month
        ]
        message_timbrados_expire_next = '*Timbrados a vencer el siguiente mes*\n\n' + '\n'.join(timbrados_information_next)
        await context.bot.send_message(chat_id=GROUP_ID, text=message_timbrados_expire_next, parse_mode=ParseMode.MARKDOWN)
