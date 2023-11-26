from view.interno import Interno
from entities.noticia import Noticia
from telegram import ParseMode, Chat
from error_handler import logging
from view.contants import *

class CindyMoon(Interno):
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)

    def notificar_noticias_automaticas(self, chat: Chat, estado_actual: bool = False, estado_anterior: bool = False) -> None:
        message = "Las noticias automáticas no están activadas."
        
        if estado_actual != estado_anterior:
            if estado_actual:
                message = "Se activaron las noticias automáticas."
            else:
                message = "Se desactivaron las noticias automáticas."
        elif estado_actual:
            message = "Las noticias automáticas ya están activadas."        

        chat.send_message(message)

    def notificar_estado(self, chat: Chat, noticias_automaticas: bool) -> None:
        chat.send_message("Noticias automáticas: {noticias_automaticas}".format(noticias_automaticas=noticias_automaticas))

    def enviar_noticia(self, chat: Chat, noticia: Noticia) -> None:
        chat.send_message(FORMATO_MENSAJE.format(titulo=noticia.titulo,
                                                descripcion=noticia.descripcion,
                                                url=noticia.url,
                                                texto_url=MAS_INFORMACION),
                  parse_mode=ParseMode.HTML)

    def ayuda(self, chat: Chat) -> None:
        chat.send_message("/noticias <n> - trae las últimas 'n' noticias\n"
                        + "/convertir <url> - convierte la noticia\n" 
                        + "/empezar - activa las noticias automáticas en el canal de noticias\n"
                        + "/terminar - desactiva las noticias automáticas en el canal de noticias\n"
                        + "/estado - muestra el estado del bot\n"
                        + "/ayuda - imprime este mensaje\n")
