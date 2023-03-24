class Clarin:
    def enviar_noticias(self, chat, noticias):
        for noticia in noticias:    
            chat.send_message("<b>" + noticia.titulo + "</b>" + "\n\n" + noticia.descripcion + "\n\n" + \
                  "<a href= \"" + noticia.url + "\">" + "MAS_INFORMACION" + "</a>\n")