import datetime
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
ARCHIVOS_LINK = MAIN_LINK + "/noticias/archivo/{year}/{month}"
FIUBA_NEWS_FILE = "fiuba_news.json"
NEWS_KEY = "news"
MAX_NEWS = 16
LENGTH_TITLE = 8
DIV_CLASS = "font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6"


class News:
    """
    Clase encargada de obtener las noticias de la página de fiuba y enviarlas a un cierto canal de Telegram.
    """
    def get_all_news_from_site(self, site) -> list:
        """
        Obtiene las noticias de la página.
        """
        page = requests.get(site)
        soup = BeautifulSoup(page.content, 'html.parser')

        return list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

    def get_message(self, link: str) -> str:
        news_page = requests.get(link)

        soup = BeautifulSoup(news_page.content, 'html.parser')

        result = soup.find('div', class_=DIV_CLASS)
        body = result.get_text().replace('\n', '')

        title = soup.title.get_text()[LENGTH_TITLE:]

        message = "<b>" + title + "</b>" + "\n\n" + body + "\n\n" + \
                  "<a href= \"" + link + "\">" + MAS_INFORMACION + "</a>\n"

        return message

    def send_news(self, chat: Chat, n_news: int, site: str) -> None:
        """
        Envía las noticias nuevas que hayan a un canal de Telegram.
        """
        news = self.get_all_news_from_site(site)

        for n in reversed(news[:n_news]):
            chat.send_chat_action(ChatAction.TYPING)
            link = MAIN_LINK + n

            message = self.get_message(link)

            chat.send_message(text=message)

            time.sleep(3)

    def send_message(self, update: Update, context: CallbackContext, link: str, command: str) -> None:
        try:
            n_news = int(context.args[0])
            if n_news <= 0:
                update.effective_chat.send_message("No puedo enviar una cantidad negativa de noticias.")
            elif n_news > MAX_NEWS:
                update.effective_chat.send_message("No puedo enviar más de " + str(MAX_NEWS) + " noticias.")
            else:
                self.send_news(update.effective_chat, n_news, link)
        except IndexError:
            update.effective_chat.send_message("Uso: {command} [cantidad de noticias]".format(command=command))
        except ValueError:
            update.effective_chat.send_message("Uso: {command} [entero positivo]".format(command=command))

    def get(self, update: Update, context: CallbackContext) -> None:
        self.send_message(update, context, NEWS_LINK, "/get")

    def get_archivo(self, update: Update, context: CallbackContext) -> None:
        month, year = datetime.date.today().month, datetime.date.today().year
        self.send_message(update, context, ARCHIVOS_LINK.format(month=month, year=year), "/archivos")

    def get_from(self, update: Update, context: CallbackContext) -> None:
        message = "Uso: /getContent [link]"

        if len(context.args) >= 1:
            if context.args[0].startswith("http://") or context.args[0].startswith("https://"):
                message = self.get_message(context.args[0])
            else:
                message = self.get_message("https://" + context.args[0])

        update.effective_chat.send_message(message)

    def status(self, update: Update, _: CallbackContext) -> None:
        chat = update.effective_chat
        chat.send_message("Esperando para enviar noticias.")
