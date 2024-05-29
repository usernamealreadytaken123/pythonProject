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
