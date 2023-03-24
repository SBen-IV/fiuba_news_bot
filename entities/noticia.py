from datetime import datetime

class Noticia:
    def __init__(self, titulo: str, descripcion: str, fecha: datetime, url: str):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.url = url