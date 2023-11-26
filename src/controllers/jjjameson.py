import os

from telegram import Update
from telegram.ext import CallbackContext
from connectors.fiuba_web import FiubaWeb
from view.imprenta import Imprenta
from view.interno import Interno
from repositories.noticias_repository import NoticiasRepository
from repositories.estado_repository import EstadoRepository
from error_handler import logging
from exceptions.cantidad_noticias_exception import CantidadNoticiasNoEsNumeroException


ID_CANAL_NOTICIAS = os.getenv('ID_CANAL_NOTICIAS')
INTERVALO_MENSAJES_AUTOMATICOS = 3*60*60  # En segundos


class JJJameson:
    def __init__(self, fiuba_web: FiubaWeb, noticias_repo: NoticiasRepository, estado_repo: EstadoRepository, imprenta: Imprenta, interno: Interno, job_queue, bot):
        self.fiuba_web = fiuba_web
        self.repo = noticias_repo
        self.estado_repo = estado_repo
        self.imprenta = imprenta
        self.interno = interno
        self.noticias_automaticas = self.estado_repo.noticias_automaticas()

        if self.noticias_automaticas:
            self.__activar_noticias_automaticas(job_queue, bot.get_chat(ID_CANAL_NOTICIAS))
        else:
            self.job = None

        self.logger = logging.getLogger(__class__.__name__)

    def conseguir_noticias(self, update: Update, context: CallbackContext):
        self.logger.info("Mensaje: {mensaje}".format(mensaje=update.effective_message.text))
        noticias = []

        try:
            if len(context.args) < 1:
                noticias = self.fiuba_web.obtener_noticias()
            else:
                cant_noticias = int(context.args[0])
                noticias = self.fiuba_web.obtener_noticias(cant_noticias)

            self.logger.info("Se consiguieron {cant_noticias} noticias.".format(cant_noticias=len(noticias)))

            self.imprenta.enviar_noticias(update.effective_chat, noticias)
        except ValueError:
            self.logger.warn("Cantidad de noticias no es número {arg}".format(arg=context.args[0]))
            raise CantidadNoticiasNoEsNumeroException(arg=context.args[0])

    def convertir_noticia(self, update: Update, context: CallbackContext):
        if len(context.args) > 0:
            noticia = self.fiuba_web.obtener_noticia(context.args[0])
            self.interno.enviar_noticia(update.effective_chat, noticia)

    def __activar_noticias_automaticas(self, job_queue, chat):
        self.job = job_queue.run_repeating(self.conseguir_noticias_automatico, INTERVALO_MENSAJES_AUTOMATICOS, context=chat)

    def activar_noticias_automaticas(self, update: Update, context: CallbackContext):
        if not self.noticias_automaticas:
            self.__activar_noticias_automaticas(context.job_queue, context.bot.get_chat(ID_CANAL_NOTICIAS))
            self.noticias_automaticas = True
            self.estado_repo.guardar(self.noticias_automaticas)
            self.logger.info("Se activaron las noticias automáticas.")
            self.interno.notificar_noticias_automaticas(update.effective_chat, self.noticias_automaticas)
        else:
            self.interno.notificar_noticias_automaticas(update.effective_chat, self.noticias_automaticas, self.noticias_automaticas)

    def desactivar_noticias_automaticas(self, update: Update, _: CallbackContext):
        if self.noticias_automaticas:
            self.job.schedule_removal()
            self.noticias_automaticas = False
            self.estado_repo.guardar(self.noticias_automaticas)
            self.logger.info("Se desactivaron las noticias automáticas.")
            self.interno.notificar_noticias_automaticas(update.effective_chat, self.noticias_automaticas, True)
        else:
            self.interno.notificar_noticias_automaticas(update.effective_chat)

    def conseguir_noticias_automatico(self, context: CallbackContext):
        ultima_noticia_guardada = self.repo.ultima_noticia()
        self.logger.info("Fecha de última noticia {titulo} es {fecha}.".format(titulo=ultima_noticia_guardada.titulo, fecha=ultima_noticia_guardada.fecha))

        nuevas_noticias = self.fiuba_web.obtener_noticias_nuevas(ultima_noticia_guardada)

        if len(nuevas_noticias) > 0:
            self.logger.info("Hay {cant_noticias} noticias nuevas.".format(cant_noticias=len(nuevas_noticias)))
            self.repo.guardar(max(nuevas_noticias, key=lambda n: n.fecha))
            self.imprenta.enviar_noticias(context.job.context, nuevas_noticias, 30)
        else:
            self.logger.info("No hay noticias nuevas.")

    def estado(self, update: Update, _: CallbackContext):
        self.interno.notificar_estado(update.effective_chat, self.noticias_automaticas)

    def ayuda(self, update: Update, context: CallbackContext):
        self.interno.ayuda(update.effective_chat)
