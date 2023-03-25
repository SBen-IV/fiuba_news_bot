import requests as requests
import dateparser as dp
from bs4 import BeautifulSoup
from connectors.fiuba_web import FiubaWeb
from error_handler import logging
from entities.noticia import Noticia
from exceptions.cantidad_noticias_exception import CantidadNoticiasMaximaException, CantidadNoticiasNegativaException

DOMINIO = "https://fi.uba.ar"
LINK_NOTICIAS = DOMINIO + "/noticias/pagina/1"
DIV_CLASS_DESCRIPCION = "font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6"
DIV_CLASS_FECHA = "mt-4 lg:mt-0 text-gray-500 text-xs uppercase"
FORMATO_FECHA = "%d de %B de %Y, %H:%M"
INICIO_TITULO = 8
MAX_NOTICIAS = 16

class Silk(FiubaWeb):
    def __init__(self):
        self.logger = logging.getLogger(__class__.__name__)

    def obtener_noticias(self,  n_noticias: int = 1) -> list:
        self.__validar_cantidad(n_noticias)

        page = requests.get(LINK_NOTICIAS)
        soup = BeautifulSoup(page.content, 'html.parser')

        uris_noticias = list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

        noticias = []

        for uri in uris_noticias[:n_noticias]:
            noticias.append(self.obtener_noticia(uri))

        return noticias
    
    def obtener_noticia(self, uri: str) -> Noticia:
        url = DOMINIO + uri
        self.logger.info("Obteniendo noticia de {url}".format(url=url))
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')

        resultado = soup.find('div', class_=DIV_CLASS_DESCRIPCION)
        descripcion = resultado.get_text().replace('\n', '')
        resultado = soup.find('div', class_=DIV_CLASS_FECHA)
        fecha = dp.parse(resultado.get_text().replace('.', ':'), date_formats=[FORMATO_FECHA], languages=['es'], locales=["es-AR"])
        self.logger.info("fecha {fecha}".format(fecha=fecha))
        self.logger.info("text {fecha}".format(fecha=resultado.get_text()))

        titulo = soup.title.get_text()[INICIO_TITULO:]

        return Noticia(titulo, descripcion, fecha, url)
    
    def __validar_cantidad(self, n_noticias: int) -> None:
        if n_noticias <= 0:
            raise CantidadNoticiasNegativaException(n_noticias)
        elif n_noticias >= MAX_NOTICIAS:
            raise CantidadNoticiasMaximaException(n_noticias)
