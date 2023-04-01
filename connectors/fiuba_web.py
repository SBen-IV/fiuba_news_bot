from abc import ABC, abstractclassmethod

from entities.noticia import Noticia

class FiubaWeb(ABC):
    
    @abstractclassmethod
    def obtener_noticias(self, n: int = 1) -> list:
        pass

    @abstractclassmethod
    def obtener_noticias_nuevas(self, ultima_noticia: Noticia) -> list:
        pass