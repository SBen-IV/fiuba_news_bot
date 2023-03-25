import time

from view.imprenta import Imprenta
from telegram import ParseMode, Chat
from emoji import emojize
from error_handler import logging

MAS_INFORMACION = emojize(":information: Más información")

class ThreatsAndMenaces(Imprenta):
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)

    def enviar_noticias(self, chat: Chat, noticias: list, delay: int = 1) -> None:
        self.logger.info("Enviando noticias a {chat_name}.".format(chat_name=chat.title))

        noticias.sort(key=lambda n: n.fecha)

        for noticia in noticias:
            chat.send_message("<b>" + noticia.titulo + "</b>" + "\n\n" + \
                               noticia.descripcion + "\n\n" + \
                  "<a href= \"" + noticia.url + "\">" + MAS_INFORMACION + "</a>\n",
                  parse_mode=ParseMode.HTML)
            
            time.sleep(delay)
