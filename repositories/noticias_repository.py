import os
import csv
from datetime import datetime

from entities.noticia import Noticia

class NoticiasRepository:
    def __init__(self, path: str = "noticias.csv"):
        if os.path.exists(path) == False:
            f = open(path, "w")
            f.close()
        self.path = path

    def ultima_noticia(self) -> Noticia:
        return Noticia("Becas SPEA-PAE: para estudiantes de Ing. en Petróleo", "La Secretaría de Inclusión, Género, Bienestar y Articulación Social (SIGBAS) de la FIUBA informa que se encuentra abierta la convocatoria para las Becas SPEA-PAE, con fecha límite de inscripción el jueves 27 de marzo de 2023, inclusive.",
                 datetime(2023, 3, 20, 14, 30, 00), "https://fi.uba.ar/noticias/becas-spea-pae")

    def guardar(self, noticia: Noticia) -> Noticia:
        return noticia