import logging
import traceback
import html
import os

from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from exceptions.cantidad_noticias_exception import *
from exceptions.url_incorrecta_exception import *

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] %(message)s', level=logging.INFO,
                    datefmt="%d/%m/%Y | %H:%M:%S")
logger = logging.getLogger('error_handler')

DEV_ID = os.getenv("DEV_ID")


def error_handler(update: Update, context: CallbackContext) -> None:
    """
    Imprime por pantalla el error y lo envía al desarrollador.
    """
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    if isinstance(context.error, CantidadNoticiasException) or isinstance(context.error, URLNoPerteneceADominioException):
        update.effective_chat.send_message(context.error.message)
    else:

        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = ''.join(tb_list)

        message = f'<pre>{html.escape(tb_string)}</pre>'

        context.bot.send_message(chat_id=DEV_ID, text=message, parse_mode=ParseMode.HTML)