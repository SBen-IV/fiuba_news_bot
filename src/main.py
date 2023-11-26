import os

from controllers.jjjameson import JJJameson
from connectors.silk import Silk
from view.threats_and_menaces import ThreatsAndMenaces
from view.cindy_moon import CindyMoon
from repositories.noticias_repository import NoticiasRepository
from repositories.estado_repository import EstadoRepository
from error_handler import error_handler, logging
from telegram.ext import Updater, Filters, CommandHandler
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

logger = logging.getLogger('main')

def main():
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)

    bot = updater.bot.get_me()

    logger.info("Iniciando {full_name} (@{username}).".format(full_name=bot.full_name, username=bot.username))

    jameson = JJJameson(Silk(), NoticiasRepository(), EstadoRepository(), ThreatsAndMenaces(), CindyMoon(), updater.job_queue, updater.bot)
    filtro = Filters.chat(chat_id=int(os.getenv('ID_GRUPO_NOTICIAS')))

    updater.dispatcher.add_handler(CommandHandler('noticias', jameson.conseguir_noticias, filtro))
    updater.dispatcher.add_handler(CommandHandler('convertir', jameson.convertir_noticia, filtro))
    updater.dispatcher.add_handler(CommandHandler('empezar', jameson.activar_noticias_automaticas, filtro))
    updater.dispatcher.add_handler(CommandHandler('terminar', jameson.desactivar_noticias_automaticas, filtro))
    updater.dispatcher.add_handler(CommandHandler('ayuda', jameson.ayuda, filtro))
    updater.dispatcher.add_handler(CommandHandler('estado', jameson.estado, filtro))
    updater.dispatcher.add_error_handler(error_handler)

    try:
        updater.start_polling()
        logger.info("Iniciado, esperando por comandos...")

        updater.idle()
    except Exception as e:
        logger.error(e.__cause__)


main()
