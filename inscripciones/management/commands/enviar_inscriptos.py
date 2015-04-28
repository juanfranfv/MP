__author__ = 'gzacur'

from django.core.management.base import BaseCommand, CommandError
from inscripciones.views import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'


    def handle(self, *args, **options):
        envio_inscriptos_parcial_view()

