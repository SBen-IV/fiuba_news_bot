from abc import ABC, abstractclassmethod
from telegram import Chat

class Imprenta(ABC):
    @abstractclassmethod
    def enviar_noticias(self, chat: Chat, noticias: list) -> None:
        pass

