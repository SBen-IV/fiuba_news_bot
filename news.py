import time

from emoji import emojize
import json
import requests as requests
from bs4 import BeautifulSoup
import os
from error_handler import logger

from telegram.ext import CallbackContext

MAS_INFORMACION = emojize(":information: Más información")
NEWS_CHAT_ID = os.getenv("NEWS_CHAT_ID")

MAIN_LINK = "https://fi.uba.ar"
NEWS_LINK = MAIN_LINK + "/noticias/pagina/1"
FIUBA_NEWS_FILE = "fiuba_news.json"
NEWS_KEY = "news"
MAX_NEWS = 16
LENGTH_TITLE = 8


class News:
    """
    Clase encargada de obtener las noticias de la página de fiuba y enviarlas a un cierto canal de Telegram.
    """
    def __init__(self):
        with open(FIUBA_NEWS_FILE, "r", encoding='UTF-8') as f:
            self.__news = json.load(f)[NEWS_KEY]

        self.__n_news = 0

    def update(self) -> None:
        """
        Actualiza las noticias de la página.
        """
        page = requests.get(NEWS_LINK)
        soup = BeautifulSoup(page.content, 'html.parser')

        new_news = list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

        diff = [n for n in new_news if n not in self.__news]

        self.__n_news = len(diff)
        diff.extend(self.__news[:MAX_NEWS-self.__n_news])
        self.__news = diff

        logger.info("{} noticias nuevas.".format(self.__n_news))

    def send_news(self, context: CallbackContext) -> None:
        """
        Envía las noticias nuevas que hayan a un canal de Telegram.
        """
        self.update()

        for n in reversed(self.__news[:self.__n_news]):
            link = MAIN_LINK + n
            news_page = requests.get(link)

            soup = BeautifulSoup(news_page.content, 'html.parser')

            result = soup.find('div',
                               class_="font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6")

            title = soup.title.get_text()[LENGTH_TITLE:]

            message = "<b>" + title + "</b>" + "\n\n" + result.get_text() + "\n\n" + \
                      "<a href= \"" + link + "\">" + MAS_INFORMACION + "</a>\n"

            msg = context.bot.send_message(chat_id=NEWS_CHAT_ID, text=message)

            context.bot.pin_chat_message(chat_id=NEWS_CHAT_ID, message_id=msg.message_id)

            time.sleep(60)

    def save(self, _: CallbackContext = None) -> None:
        """
        Guarda las noticias en un archivo json
        """
        dict_news = {"news": self.__news}
        with open(FIUBA_NEWS_FILE, "w", encoding='UTF-8') as f:
            json.dump(dict_news, f, indent=4)

        logger.info("Noticias guardadas.")
