import os
from controllers.jjjameson import JJJameson
from connectors.silk import Silk
from view.threats_and_menaces import ThreatsAndMenaces

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()

from telegram.ext import Updater, Filters, CommandHandler
    

def main():
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)

    jameson = JJJameson(Silk(), ThreatsAndMenaces())

    updater.dispatcher.add_handler(CommandHandler('noticias', jameson.conseguir_noticias, Filters.chat_type.groups))

    try:
        updater.start_polling()
        
        updater.idle()
    except Exception as e:
        print(e.__cause__)


main()