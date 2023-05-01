import os
import json

ESTADO_DEFAULT_JSON = {
    "noticias_automaticas": False
}


class EstadoRepository:
    def __init__(self, path: str = "estado.json"):
        if not os.path.exists(path):
            with open(path, "w", encoding='utf-8') as f:
                json.dump(ESTADO_DEFAULT_JSON, f, indent=4)

        self.path = path

    def noticias_automaticas(self) -> bool:
        estado = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            estado = json.load(f)

        return estado.get("noticias_automaticas", False)

    def guardar(self, noticias_automaticas) -> None:
        estado = {
             "noticias_automaticas": noticias_automaticas
        }

        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(estado, f, indent=4)
