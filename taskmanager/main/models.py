from django.db import models

# Create your models here.

class Users(models.Model):
    login = models.CharField('login', max_length=255)
    password = models.CharField('password', max_length=255)
    def __str__(self):
        return self.login

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Tasks(models.Model):
    name = models.CharField('name', max_length=255)
    time = models.CharField('time', max_length=255)
    stand = models.CharField('stand', max_length=255)
    work_type = models.CharField('work_type', max_length=255)

    def __str__(self):
        return f"{self.name} - {self.work_type}"

    class Meta:
        verbose_name = 'task'
        verbose_name_plural = 'tasks'
        db_table = 'my_table_1'  # Указываем конкретное имя таблицы
