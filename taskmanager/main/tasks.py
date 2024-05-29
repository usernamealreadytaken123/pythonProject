# main/tasks.py
from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

@shared_task
def logout_user(user_id):
    try:
        user = User.objects.get(pk=user_id)
        # Удаляем все сессии пользователя
        for session in Session.objects.all():
            if session.get_decoded().get('_auth_user_id') == str(user_id):
                session.delete()
    except User.DoesNotExist:
        pass
