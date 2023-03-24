from telegram import Update
from telegram.ext import CallbackContext
from connectors.fiuba_web import FiubaWeb
from view.imprenta import Imprenta
from error_handler import logging

class JJJameson:
    def __init__(self, fiuba_web: FiubaWeb, imprenta: Imprenta):
        self.fiuba_web = fiuba_web
        self.imprenta = imprenta
        self.logger = logging.getLogger(__class__.__name__)

    def conseguir_noticias(self, update: Update, _: CallbackContext):
        self.logger.info("Mensaje: {mensaje}".format(mensaje=update.effective_message.text))
        noticias = self.fiuba_web.obtener_noticias()

        self.logger.info("Se consiguieron {n_noticias} noticias.".format(n_noticias=len(noticias)))

        self.imprenta.enviar_noticias(update.effective_chat, noticias)
