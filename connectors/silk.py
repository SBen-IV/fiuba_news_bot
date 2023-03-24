import requests as requests
from bs4 import BeautifulSoup
from connectors.fiuba_web import FiubaWeb

from entities.noticia import Noticia

DOMINIO = "https://fi.uba.ar"
LINK_NOTICIAS = DOMINIO + "/noticias/pagina/1"
DIV_CLASS = "font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6"
INICIO_TITULO = 8

class Silk(FiubaWeb):
    def obtener_noticias(self,  n: int = 1) -> list:
        page = requests.get(LINK_NOTICIAS)
        soup = BeautifulSoup(page.content, 'html.parser')

        uris_noticias = list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

        noticias = []

        for uri in uris_noticias[:n]:
            noticias.append(self.obtener_noticia(uri))

        return noticias
    
    def obtener_noticia(self, uri: str) -> Noticia:
        url = DOMINIO + uri
        print("request a " + url)
        pagina = requests.get(url)
        soup = BeautifulSoup(pagina.content, 'html.parser')

        resultado = soup.find('div', class_=DIV_CLASS)
        descripcion = resultado.get_text().replace('\n', '')

        titulo = soup.title.get_text()[INICIO_TITULO:]

        return Noticia(titulo, descripcion, url)