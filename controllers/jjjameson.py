from telegram import Update
from telegram.ext import CallbackContext
from connectors.fiuba_web import FiubaWeb
from view.imprenta import Imprenta


class JJJameson:
    def __init__(self, fiuba_web: FiubaWeb, imprenta: Imprenta):
        self.fiuba_web = fiuba_web
        self.imprenta = imprenta

    def conseguir_noticias(self, update: Update, _: CallbackContext):
        noticias = self.fiuba_web.obtener_noticias()

        self.imprenta.enviar_noticias(update.effective_chat, noticias)
