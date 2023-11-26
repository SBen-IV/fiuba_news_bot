from abc import ABC, abstractclassmethod
from telegram import Chat
from entities.noticia import Noticia

class Interno(ABC):
    @abstractclassmethod
    def notificar_noticias_automaticas(self, chat: Chat, estado_actual: bool, estado_anterior: bool) -> None:
        pass

    @abstractclassmethod
    def notificar_estado(self, chat: Chat, noticias_automaticas: bool) -> None:
        pass

    @abstractclassmethod
    def enviar_noticia(self, chat: Chat, noticia: Noticia) -> None:
        pass

    @abstractclassmethod
    def ayuda(self, chat: Chat) -> None:
        pass
