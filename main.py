import os
from controllers.jjjameson import JJJameson
from connectors.silk import Silk
from view.clarin import Clarin

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

from telegram import ParseMode
from telegram.ext import Updater, Filters, CommandHandler, Defaults
    

def main():
    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True, defaults=defaults)

    jameson = JJJameson(Silk(), Clarin())

    updater.dispatcher.add_handler(CommandHandler('noticias', jameson.conseguir_noticias, Filters.chat_type.groups))

    try:
        updater.start_polling()
        
        updater.idle()
    except Exception as e:
        print(e.__cause__)


main()