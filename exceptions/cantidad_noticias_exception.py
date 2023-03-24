class CantidadNoticiasException(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)

class CantidadNoticiasNoEsNumeroException(CantidadNoticiasException):
    def __init__(self, arg = "") -> None:
        self.message = "No creo que '{arg}' sea un número.".format(arg=arg)
        super().__init__(self.message)
    
class CantidadNoticiasNegativaException(CantidadNoticiasException):
    def __init__(self, arg) -> None:
        self.message = "¿Cómo puedo conseguir {arg} noticias?".format(arg=arg)
        super().__init__(self.message)

class CantidadNoticiasMaximaException(CantidadNoticiasException):
    def __init__(self, arg) -> None:
        self.message = "¿Quieres que consiga {arg} noticias? Aumentame el sueldo.".format(arg=arg)
        super().__init__(self.message)
