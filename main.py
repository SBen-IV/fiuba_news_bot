import os
from controllers.jjjameson import JJJameson
from connectors.silk import Silk
from view.threats_and_menaces import ThreatsAndMenaces
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

    jameson = JJJameson(Silk(), ThreatsAndMenaces())

    updater.dispatcher.add_handler(CommandHandler('noticias', jameson.conseguir_noticias, Filters.chat_type.groups))
    updater.dispatcher.add_handler(CommandHandler('empezar', jameson.activar_noticias_automaticas, Filters.chat_type.groups))
    updater.dispatcher.add_handler(CommandHandler('terminar', jameson.desactivar_noticias_automaticas, Filters.chat_type.groups))
    updater.dispatcher.add_error_handler(error_handler)

    try:
        updater.start_polling()
        logger.info("Iniciado, esperando por comandos...")
        
        updater.idle()
    except Exception as e:
        logger.error(e.__cause__)


main()