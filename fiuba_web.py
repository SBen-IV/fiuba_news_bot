import requests as requests
from bs4 import BeautifulSoup
import logging

from news import News

DOMINIO = "https://fi.uba.ar"
LINK_NOTICIAS = DOMINIO + "/noticias/pagina/1"
DIV_CLASS = "font-light text-lg leading-relaxed border-b border-border-soft-color pb-8 mb-6"
LENGTH_TITLE = 8

class FiubaWeb:
    def obtener_noticias(self) -> list:
        page = requests.get(LINK_NOTICIAS)
        soup = BeautifulSoup(page.content, 'html.parser')

        uris_noticias = list(map(lambda x: x.get('href'), soup.select(".noticia > a")))

        noticias = []

        for uri in uris_noticias[:1]:
            noticias.append(self.obtener_noticia(uri))

        return noticias
    
    def obtener_noticia(self, uri) -> News:
        print("request a " + DOMINIO + uri)
        pagina = requests.get(DOMINIO + uri)
        soup = BeautifulSoup(pagina.content, 'html.parser')

        resultado = soup.find('div', class_=DIV_CLASS)
        descripcion = resultado.get_text().replace('\n', '')

        titulo = soup.title.get_text()[LENGTH_TITLE:]

        return News(titulo=titulo, descripcion=descripcion, url=DOMINIO + uri)