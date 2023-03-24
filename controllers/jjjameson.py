from telegram import Update
from telegram.ext import CallbackContext
from connectors.fiuba_web import FiubaWeb
from view.imprenta import Imprenta
from error_handler import logging
from exceptions.cantidad_noticias_exception import CantidadNoticiasNoEsNumeroException

class JJJameson:
    def __init__(self, fiuba_web: FiubaWeb, imprenta: Imprenta):
        self.fiuba_web = fiuba_web
        self.imprenta = imprenta
        self.logger = logging.getLogger(__class__.__name__)

    def conseguir_noticias(self, update: Update, context: CallbackContext):
        self.logger.info("Mensaje: {mensaje}".format(mensaje=update.effective_message.text))
        noticias = []

        try:
            if len(context.args) < 1:
                noticias = self.fiuba_web.obtener_noticias()
            else:
                n_noticias = int(context.args[0])
                noticias = self.fiuba_web.obtener_noticias(n_noticias)

            self.logger.info("Se consiguieron {n_noticias} noticias.".format(n_noticias=len(noticias)))

            self.imprenta.enviar_noticias(update.effective_chat, noticias)
        except ValueError:
            self.logger.warn("Cantidad de noticias no es numero {arg}".format(arg=context.args[0]))
            raise CantidadNoticiasNoEsNumeroException(arg=context.args[0])
