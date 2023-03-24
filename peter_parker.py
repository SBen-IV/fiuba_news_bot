from telegram import Update
from telegram.ext import CallbackContext


class PeterParker:
    def __init__(self, fiuba_web, imprenta):
        self.fiuba_web = fiuba_web
        self.imprenta = imprenta

    def conseguir_noticias(self, update: Update, _: CallbackContext):
        noticias = self.fiuba_web.obtener_noticias()

        self.imprenta.enviar_noticias(update.effective_chat, noticias)
