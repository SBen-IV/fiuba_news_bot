import logging
import traceback
import html
import os

from telegram import Update
from telegram.ext import CallbackContext

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s', level=logging.INFO,
                    datefmt="%d/%m/%Y | %H:%M:%S")
logger = logging.getLogger(__name__)

DEV_ID = os.getenv("DEV_ID")


def error_handler(_: Update, context: CallbackContext) -> None:
    """
    Imprime por pantalla el error y lo envía al desarrollador.
    """
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    message = f'<pre>{html.escape(tb_string)}</pre>'

    context.bot.send_message(chat_id=DEV_ID, text=message)
