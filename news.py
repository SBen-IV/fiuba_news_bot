import time

from emoji import emojize
import requests as requests
from bs4 import BeautifulSoup
import os

from telegram import Update, Chat, ChatAction

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
DIV_CLASS = "font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6"


class News:
    """
    Clase encargada de obtener las noticias de la página de fiuba y enviarlas a un cierto canal de Telegram.
    """
    def get_all_news_from_site(self) -> list:
        """
        Obtiene las noticias de la página.
        """
        page = requests.get(NEWS_LINK)
        soup = BeautifulSoup(page.content, 'html.parser')

        return list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

    def send_news(self, chat: Chat, n_news: int) -> None:
        """
        Envía las noticias nuevas que hayan a un canal de Telegram.
        """
        news = self.get_all_news_from_site()

        for n in reversed(news[:n_news]):
            chat.send_chat_action(ChatAction.TYPING)
            link = MAIN_LINK + n
            news_page = requests.get(link)

            soup = BeautifulSoup(news_page.content, 'html.parser')

            result = soup.find('div', class_=DIV_CLASS)
            body = result.get_text().replace('\n', '')

            title = soup.title.get_text()[LENGTH_TITLE:]

            message = "<b>" + title + "</b>" + "\n\n" + body + "\n\n" + \
                      "<a href= \"" + link + "\">" + MAS_INFORMACION + "</a>\n"

            chat.send_message(text=message)

            time.sleep(3)

    def get(self, update: Update, context: CallbackContext) -> None:
        try:
            n_news = int(context.args[0])
            if n_news <= 0:
                update.effective_chat.send_message("No puedo enviar una cantidad negativa de noticias.")
            elif n_news > MAX_NEWS:
                update.effective_chat.send_message("No puedo enviar más de " + str(MAX_NEWS) + " noticias.")
            else:
                self.send_news(update.effective_chat, n_news)
        except IndexError:
            update.effective_chat.send_message("Uso: /get [cantidad de noticias]")
        except ValueError:
            update.effective_chat.send_message("Uso: /get [entero positivo]")

    def status(self, update: Update, _: CallbackContext) -> None:
        chat = update.effective_chat
        chat.send_message("Esperando para enviar noticias.")
