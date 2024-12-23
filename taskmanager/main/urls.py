"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import profile

from django.urls import path
from .import views


urlpatterns = [
    path('', views.auth, name='auth'),

    ##path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('auth/', views.auth, name='auth'),
    path('book/', views.book, name='book'),
    path('list_reg/', views.list_reg, name='list_reg'),
    path('tasks_list/', views.tasks_list, name='tasks_list'),
    path('update_stand_status_forever/', views.update_stand_status_forever, name='stand_reg'),

]
