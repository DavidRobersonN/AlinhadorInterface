from django.apps import AppConfig
import os


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    _started = False

    def ready(self):
        # Evita iniciar duas vezes
        if CoreConfig._started:
            return

        # No runserver com autoreload, isso ajuda a evitar duplicação
        if os.environ.get("RUN_MAIN") != "true":
            return

        from .serial_manager import start_serial_listener
        start_serial_listener()
        CoreConfig._started = True