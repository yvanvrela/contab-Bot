import re
import os
import random
import asyncio
from telegram import Update
from utils.export_files import xls_to_txt, scan_files, read_file, write_file, to_zip, delete_file
from services.marangatu_scraper.baja_timbrado import document_util

async def export_files_r90(update: Update, context):
    chat_id = update.message.chat_id

    msg_buscar_list = ['Buscando archivos... 🔍', 'Buscando voy 🔍, yo por las carpetas... 🎶🎶']
    msg_buscar = random.choice(msg_buscar_list)

    await context.bot.send_message(chat_id=chat_id, text=msg_buscar)

    await asyncio.to_thread(xls_to_txt)
    files = await asyncio.to_thread(scan_files)

    month_names = {
        '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
        '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
        '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre',
    }

    if files:
        files_name = ''
        for file in files:
            client_name = re.findall('/([a-z]+)/', file)[0]
            month = month_names[re.findall('/([0-9]{2})/', file)[0]]
            search_year = re.findall('/([0-9]{4})/', file)

            if len(search_year) >= 1:
                year = search_year[0]
            else:
                year = 'Sin año'

            file_name = re.findall('\w+.txt', file)
            name = file_name[0]
            month_and_year = f'{month} - {year}'

            if client_name.capitalize() in files_name:
                if month_and_year in files_name:
                    files_name += f'{name}\n'
                else:
                    files_name += f'{month_and_year}\n{name}\n'
            else:
                files_name += f'{client_name.capitalize()}:\n{month_and_year}\n{name}\n'

        await context.bot.send_message(chat_id=chat_id, text=f'{files_name} \n  Encontré estos archivos')

        for file in files:
            file_content = await asyncio.to_thread(read_file, file)
            await asyncio.to_thread(write_file, file_content, path=file)
            await asyncio.to_thread(to_zip, file)
            await asyncio.to_thread(delete_file, file)

        await context.bot.send_message(chat_id=chat_id, text='Exportados a zip, listos para enviar 🦖')
    else:
        await context.bot.send_message(chat_id=chat_id, text='No hay archivos nuevos :(')

async def export_anulados(update: Update, context):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Buscando facturas anuladas... 🔍')

    # Separate anulados data and write to new txt file
    anulados_files_path = await asyncio.to_thread(document_util.separate_anulados)
    path_anulados = os.environ.get('PATH_ANULADOS', 'Z:/anulados')
    anulados_files_path = await asyncio.to_thread(scan_files, file_extension='.txt', raiz_dir=path_anulados)
    print(anulados_files_path)
