class URLNoPerteneceADominioException(Exception):
    def __init__(self, dominio, url) -> None:
        self.message = "{url} no pertenece al dominio {dominio}".format(url=url, dominio=dominio)
        super().__init__(self.message)