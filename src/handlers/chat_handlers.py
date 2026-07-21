import re
import asyncio
from random import randint
from time import sleep
from telegram import Update
from utils import office_require
from services.chatgpt.chatGPT_chat import bot_response
from utils.messages_list import *

def msjAleatorio(listMsj: list) -> int:
    endMsj = len(listMsj) - 1
    positionMsj = randint(0, endMsj)
    return positionMsj

async def echo(update: Update, context):
    # Busca una palabra clave, y responde con un mensaje
    chat_id = update.message.chat_id
    message = update.message.text.lower()

    user = update.message.from_user

    items = re.findall('^falta.+', message)

    if len(items) > 0:
        office_require.add_items(items[0])
        await update.message.reply_text('Ok, agregados a la lista')

    if message == 'qué falta?' or message == 'que falta?':
        await update.message.reply_text('Voy a buscar')
        await asyncio.sleep(1)
        items = office_require.read_items()
        items_message = ''
        if len(items) > 0:
            await update.message.reply_text('Encontré que falta')
            for item in items:
                items_message += f'El {item["date"]}\n'
                for i in item["items"]:
                    items_message += f'{i.strip()}\n'
                items_message += '\n'
            await update.message.reply_text(items_message)
        else:
            await update.message.reply_text('No hay nada en falta 👍')

    if message == 'comprado':
        await update.message.reply_text('Ok, borro datos de la lista 👌')
        office_require.delete_items()

    if message in agradecimientos:
        response = reply_agradecimientos[msjAleatorio(reply_agradecimientos)]
        await update.message.reply_text(response)

    elif message in cumplidos:
        username = user.first_name
        response = await asyncio.to_thread(bot_response, prompt=f'{username}: {message}', temperature=0.9)
        if response:
            await update.message.reply_text(response)

    elif message in regaños:
        response = reply_regaños[msjAleatorio(reply_regaños)]
        await update.message.reply_text(response)

    elif 'hola' in message:
        username = user.first_name
        response = await asyncio.to_thread(bot_response, prompt=f'{username}: {message}', temperature=0.9)
        if response:
            await update.message.reply_text(response)

    elif message in nombres:
        respuestas = ['Si?', '🫡', 'Soy yo', '👀', 'Qué paso wey?', '😶‍🌫️']
        await update.message.reply_text(respuestas[msjAleatorio(respuestas)])

    elif message == 'benitooo':
        await update.message.reply_text('QUEE!!!')

    elif message in preguntas_quehacer:
        response = reply_quehacer[msjAleatorio(reply_quehacer)]
        await update.message.reply_text(response)

    elif message in afirmaciones:
        reply = 'Sii'
        await context.bot.send_message(chat_id=chat_id, text=reply)

    elif message in despedidas:
        response = reply_despedidas[msjAleatorio(reply_despedidas)]
        await update.message.reply_text(response)

    elif message in saludos:
        response = reply_saludos[msjAleatorio(reply_saludos)]
        await update.message.reply_text(response)

    if 'jaja' in message:
        await context.bot.send_message(chat_id=chat_id, text=message.capitalize())

    if 'chaa' in message:
        reply = message.capitalize()
        await context.bot.send_message(chat_id=chat_id, text=reply)
