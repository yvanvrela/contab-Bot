from telegram import Update
from telegram.ext import ConversationHandler

async def start(update: Update, context):
    """Mensaje de Inicio"""
    await update.message.reply_text('Hola!')

async def help_command(update: Update, context):
    """Lista de Funciones"""
    await update.message.reply_text(
        """
        Funciones para el control de los Clientes.
    /nuevocliente - agregar cliente
    /listaclientes - ver todos los clientes

    Configuración de Clientes
    /agregartimbrado - agregar un nuevo timbrado
    /recepciondocumentos - resive los documentos
    /retirodocumentos - nose
    /colorcarpeta - agregar el color
    /export - exportar archivos de la R-90
    /buscarci - Busca el n° de documente en el RUC
    /

    Falta más funciones, pero aprendo rápido."""
    )

async def done(update: Update, context) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text('Oc')
    user_data.clear()
    return ConversationHandler.END
