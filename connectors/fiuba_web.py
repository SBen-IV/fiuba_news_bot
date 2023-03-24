from abc import ABC, abstractclassmethod

from entities.noticia import Noticia

class FiubaWeb(ABC):
    
    @abstractclassmethod
    def obtener_noticias(self, n: int = 1) -> list:
        pass