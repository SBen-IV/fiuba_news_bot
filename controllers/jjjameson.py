import os

from telegram import Update
from telegram.ext import CallbackContext
from connectors.fiuba_web import FiubaWeb
from view.imprenta import Imprenta
from repositories.noticias_repository import NoticiasRepository
from error_handler import logging
from exceptions.cantidad_noticias_exception import CantidadNoticiasNoEsNumeroException


ID_CANAL_NOTICIAS = os.getenv('ID_CANAL_NOTICIAS')
INTERVALO_MENSAJES_AUTOMATICOS = 3*60*60 # En segundos

class JJJameson:
    def __init__(self, fiuba_web: FiubaWeb, repo: NoticiasRepository, imprenta: Imprenta):
        self.fiuba_web = fiuba_web
        self.repo = repo
        self.imprenta = imprenta
        self.noticias_automaticas = False
        self.job = None
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

            self.logger.info("ID chat: {id}".format(id=update.effective_chat.id))
            self.imprenta.enviar_noticias(update.effective_chat, noticias)
        except ValueError:
            self.logger.warn("Cantidad de noticias no es numero {arg}".format(arg=context.args[0]))
            raise CantidadNoticiasNoEsNumeroException(arg=context.args[0])

    def activar_noticias_automaticas(self, update: Update, context: CallbackContext):
        if self.noticias_automaticas == False:
            self.job = context.job_queue.run_repeating(self.conseguir_noticias_automatico, INTERVALO_MENSAJES_AUTOMATICOS, context=context.bot.get_chat(ID_CANAL_NOTICIAS))
            self.noticias_automaticas = True
            self.logger.info("Se activaron las noticias automaticas.")
            update.effective_chat.send_message("Se activaron las noticias automaticas.")
        else:
            update.effective_chat.send_message("Las noticias automaticas ya estan activadas.")
            

    def desactivar_noticias_automaticas(self, update: Update, context: CallbackContext):
        if self.noticias_automaticas == True:
            self.job.schedule_removal()
            self.noticias_automaticas = False
            self.logger.info("Se desactivaron las noticias automaticas.")
            update.effective_chat.send_message("Se desactivaron las noticias automaticas.")
        else:
            update.effective_chat.send_message("Las noticias automaticas no estan activadas.")

    def conseguir_noticias_automatico(self, context: CallbackContext):
        ultima_noticia_guardada = self.repo.ultima_noticia()
        ultimas_noticias = self.fiuba_web.obtener_noticias(15)

        self.logger.info("fecha de ultima noticia {titulo} es {fecha}.".format(titulo=ultima_noticia_guardada.titulo, fecha=ultima_noticia_guardada.fecha))

        nuevas_noticias = []
        for noticia in ultimas_noticias:
            if noticia.fecha > ultima_noticia_guardada.fecha:
                self.logger.info("fecha de noticia {titulo} es {fecha}".format(titulo=noticia.titulo, fecha=noticia.fecha))
                nuevas_noticias.append(noticia)
        
        if len(nuevas_noticias) > 0:
            self.repo.guardar(max(nuevas_noticias, key=lambda n: n.fecha))
        
        self.imprenta.enviar_noticias(context.job.context, nuevas_noticias, 30)
