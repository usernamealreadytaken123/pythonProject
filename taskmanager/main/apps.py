# apps.py
from django.apps import AppConfig
import threading

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .views import update_stand_status_forever  # Импорт внутри функции
        thread = threading.Thread(target=update_stand_status_forever, daemon=True)
        thread.start()
