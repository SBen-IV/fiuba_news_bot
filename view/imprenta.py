from abc import ABC, abstractclassmethod

class Imprenta(ABC):
    @abstractclassmethod
    def enviar_noticias(self, chat, noticias) -> None:
        pass

