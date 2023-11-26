import time

from view.imprenta import Imprenta
from telegram import ParseMode, Chat
from error_handler import logging
from view.contants import *

class ThreatsAndMenaces(Imprenta):
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)

    def enviar_noticias(self, chat: Chat, noticias: list, delay: int = 1) -> None:
        self.logger.info("Enviando noticias a {chat_name}.".format(chat_name=chat.title))

        noticias.sort(key=lambda n: n.fecha)

        for noticia in noticias:
            chat.send_message(FORMATO_MENSAJE.format(titulo=noticia.titulo,
                                                     descripcion=noticia.descripcion,
                                                     url=noticia.url,
                                                     texto_url=MAS_INFORMACION),
                  parse_mode=ParseMode.HTML)
            
            time.sleep(delay)
