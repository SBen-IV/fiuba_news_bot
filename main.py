import pytz
from dotenv import load_dotenv
import os

if os.path.exists(".env"):
    load_dotenv()

import datetime as dtm
from news import News
from error_handler import logger, error_handler

from telegram import ParseMode
from telegram.ext import Updater, Defaults, Filters, CommandHandler

FIRST_REPEATING = dtm.time(7, 0, 0)
LAST_REPEATING = dtm.time(23, 5, 0)
TIME_DAILY_SEND_NEWS = dtm.time(6, 0, 0)
TIME_DAILY_SAVE_NEWS = dtm.time(1, 0, 0)
# Minutos * segundos
INTERVAL_REPEATING = 60*60
TIME_ZONE = pytz.timezone('America/Argentina/Buenos_Aires')


def main():
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=TIME_ZONE)

    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, defaults=defaults)

    bot = updater.bot.get_me()

    logger.info("Iniciando " + bot.full_name + " (@" + bot.username + ")")

    news = News()

    updater.dispatcher.add_handler(CommandHandler(['get', 'noticias'], news.get, Filters.chat_type.groups))
    updater.dispatcher.add_handler(CommandHandler('archivos', news.get_archivo, Filters.chat_type.groups))
    updater.dispatcher.add_handler(CommandHandler('getFrom', news.get_from, Filters.chat_type.groups))
    updater.dispatcher.add_handler(CommandHandler('status', news.status, Filters.chat_type.private))
    updater.dispatcher.add_error_handler(error_handler)

    try:
        updater.start_polling()
        logger.info("Iniciado.")

        updater.idle()
    except Exception as e:
        logger.error(e.__cause__)

    logger.info("Finalizado.")


if __name__ == "__main__":
    main()
