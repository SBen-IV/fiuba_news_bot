from view.imprenta import Imprenta
from telegram import ParseMode
from emoji import emojize

MAS_INFORMACION = emojize(":information: Más información")

class ThreatsAndMenaces(Imprenta):
    def enviar_noticias(self, chat, noticias) -> None:
        for noticia in noticias:    
            chat.send_message("<b>" + noticia.titulo + "</b>" + "\n\n" + noticia.descripcion + "\n\n" + \
                  "<a href= \"" + noticia.url + "\">" + MAS_INFORMACION + "</a>\n",
                  parse_mode=ParseMode.HTML)
