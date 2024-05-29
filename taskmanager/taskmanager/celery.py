# # taskmanager/celery.py
# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # Установите настройки по умолчанию Django для Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
#
# app = Celery('taskmanager')
#
# # Загрузите конфигурацию из настроек Django, используя пространство имен `CELERY`
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Автоматически обнаруживайте задачи в установленных приложениях Django
# app.autodiscover_tasks()
#
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
