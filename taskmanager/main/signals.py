# # main/signals.py
# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from .tasks import logout_user
# import redis
# @receiver(user_logged_in)
# def user_logged_in_handler(sender, request, user, **kwargs):
#     # Запуск задачи Celery на разлогин через 1 минуту
#     logout_user.apply_async((user.id,), countdown=60)
