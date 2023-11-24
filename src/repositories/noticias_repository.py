import os
import json
from datetime import datetime

from entities.noticia import Noticia
from error_handler import logging


class NoticiasRepository:
    def __init__(self, path: str = "noticias.json"):
        if not os.path.exists(path):
            f = open(path, "w")
            f.close()
        self.path = path
        self.logger = logging.getLogger(__class__.__name__)

    def ultima_noticia(self) -> Noticia:
        ultima_noticia_json = {}

        with open(self.path, 'r', encoding='utf-8') as f:
            ultima_noticia_json = json.load(f)

        return self.__json_to_object(ultima_noticia_json)

    def guardar(self, noticia: Noticia) -> Noticia:
        noticia_json = self.__object_to_json(noticia)

        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(noticia_json, f, indent=4)

        self.logger.info("Guardada {noticia}.".format(noticia=noticia_json))

        return noticia

    def __object_to_json(self, noticia: Noticia) -> dict:
        noticia_json = {
            "titulo": noticia.titulo,
            "descripcion": noticia.descripcion,
            "fecha": noticia.fecha.strftime("%Y-%m-%d %H:%M"),
            "url": noticia.url
        }

        return noticia_json

    def __json_to_object(self, noticia_json: dict) -> Noticia:
        fecha = datetime.strptime(noticia_json['fecha'], "%Y-%m-%d %H:%M")
        return Noticia(noticia_json['titulo'], noticia_json['descripcion'], fecha, noticia_json['url'])
