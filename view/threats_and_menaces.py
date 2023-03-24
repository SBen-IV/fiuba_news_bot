from view.imprenta import Imprenta
from telegram import ParseMode, Chat
from emoji import emojize
from error_handler import logging

MAS_INFORMACION = emojize(":information: Más información")

class ThreatsAndMenaces(Imprenta):
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)

    def enviar_noticias(self, chat: Chat, noticias: list) -> None:
        self.logger.info("Enviando noticias a {chat_name}.".format(chat_name=chat.title))

        for noticia in reversed(noticias):
            chat.send_message("<b>" + noticia.titulo + "</b>" + "\n\n" + \
                               noticia.descripcion + "\n\n" + \
                  "<a href= \"" + noticia.url + "\">" + MAS_INFORMACION + "</a>\n",
                  parse_mode=ParseMode.HTML)
