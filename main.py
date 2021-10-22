import json

from dotenv import load_dotenv
import os
import time

import requests as requests
from bs4 import BeautifulSoup

from telegram import ParseMode
from emoji import emojize
from telegram.ext import Updater, CallbackContext

if os.path.exists(".env"):
    load_dotenv()

MAS_INFORMACION = emojize(':plus: Más información')
NEWS_CHAT_ID = os.getenv("NEWS_CHAT_ID")

MAIN_LINK = 'https://fi.uba.ar'
FIUBA_NEWS_FILE = "fiuba_news.json"
NEWS_KEY = "news"
MAX_NEWS = 16


class News:
    def __init__(self):
        with open(FIUBA_NEWS_FILE, "r", encoding='UTF-8') as f:
            self.__news = json.load(f)[NEWS_KEY]

        self.__n_news = 0

    def update(self):
        page = requests.get('https://fi.uba.ar/noticias/pagina/1')
        soup = BeautifulSoup(page.content, 'html.parser')

        new_news = list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

        diff = [n for n in new_news if n not in self.__news]

        self.__n_news = len(diff)
        diff.extend(self.__news[:MAX_NEWS-self.__n_news])
        self.__news = diff

        print("{} noticias nuevas.".format(self.__n_news))

    def send_news(self, context: CallbackContext):
        self.update()

        for n in reversed(self.__news[:self.__n_news]):
            link = MAIN_LINK + n
            news_page = requests.get(link)

            soup = BeautifulSoup(news_page.content, 'html.parser')

            result = soup.find('div',
                               class_="font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6")

            title = soup.title.get_text()[8:]

            message = "<b>" + title + "</b>" + "\n\n" + result.get_text() + "\n\n" + \
                      "<a href= \"" + link + "\">" + MAS_INFORMACION + "</a>\n"

            msg = context.bot.send_message(chat_id=NEWS_CHAT_ID, text=message, parse_mode=ParseMode.HTML)

            context.bot.pin_chat_message(chat_id=NEWS_CHAT_ID, message_id=msg.message_id)

            time.sleep(5)

    def save(self):
        dict_news = {"news": self.__news}
        with open(FIUBA_NEWS_FILE, "w", encoding='UTF-8') as f:
            json.dump(dict_news, f, indent=4)


def main():
    updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)

    bot = updater.bot.get_me()

    print("Iniciando " + bot.full_name + " (@" + bot.username + ")")

    news = News()
    # Cada 1 hs
    updater.job_queue.run_repeating(news.send_news, 3600, first=10)

    print("Iniciado.")
    updater.start_polling()

    updater.idle()

    print("Guardando...")
    news.save()

    print("Finalizado.")


if __name__ == "__main__":
    main()
