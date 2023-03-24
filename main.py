import os
from peter_parker import PeterParker
from fiuba_web import FiubaWeb
from clarin import Clarin

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

from telegram import ParseMode
from telegram.ext import Updater, Filters, CommandHandler, Defaults
    

def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, defaults=defaults)

    peter = PeterParker(FiubaWeb(), Clarin())

    updater.dispatcher.add_handler(CommandHandler('noticias', peter.conseguir_noticias, Filters.chat_type.groups))

    try:
        updater.start_polling()
        
        updater.idle()
    except Exception as e:
        print(e.__cause__)


main()