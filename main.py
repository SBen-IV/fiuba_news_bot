import pytz
from dotenv import load_dotenv
import os

if os.path.exists(".env"):
    load_dotenv()

import datetime as dtm
from news import News
from error_handler import logger, error_handler

from telegram import ParseMode
from telegram.ext import Updater, Defaults, CallbackContext, Job, Dispatcher

FIRST_REPEATING = dtm.time(7, 0, 0)
LAST_REPEATING = dtm.time(23, 5, 0)
TIME_DAILY_SEND_NEWS = dtm.time(6, 0, 0)
TIME_DAILY_SAVE_NEWS = dtm.time(1, 0, 0)
# Minutos * segundos
INTERVAL_REPEATING = 60*60
TIME_ZONE = pytz.timezone('America/Argentina/Buenos_Aires')


def set_send_news_job(context: CallbackContext) -> None:
    """
    Establece un job para obtener las noticias del día de la página.
    """
    context.job_queue.run_repeating(context.job.context.send_news, INTERVAL_REPEATING, first=FIRST_REPEATING,
                                    last=LAST_REPEATING)
    logger.info("Programado send_news de hoy.")


def run_job(daily_job: Job, dispatcher: Dispatcher) -> None:
    """
    Corre daily_job en caso que se haya ejecutado dentro de la hora de TIME_DAILY_SEND_NEWS y LAST_REPEATING.
    """
    now = dtm.datetime.now(TIME_ZONE)

    if TIME_DAILY_SEND_NEWS.hour < now.hour < LAST_REPEATING.hour:
        daily_job.run(dispatcher)


def main():
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=TIME_ZONE)

    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, defaults=defaults)

    bot = updater.bot.get_me()

    logger.info("Iniciando " + bot.full_name + " (@" + bot.username + ")")

    news = News()

    daily_job = updater.job_queue.run_daily(set_send_news_job, TIME_DAILY_SEND_NEWS, context=news)
    updater.job_queue.run_daily(news.save, TIME_DAILY_SAVE_NEWS)

    updater.dispatcher.add_error_handler(error_handler)
    try:
        updater.start_polling()
        logger.info("Iniciado.")

        run_job(daily_job, updater.dispatcher)

        updater.idle()
    except Exception as e:
        logger.error(e.__cause__)

    logger.info("Guardando...")
    news.save()

    logger.info("Finalizado.")


if __name__ == "__main__":
    main()
