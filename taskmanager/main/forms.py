from .models import Users, Tasks
from django.forms import ModelForm, TextInput, Textarea, ChoiceField
from datetime import time, timedelta
from django import forms

def generate_time_choices():
    """Генерирует список времени с шагом 1.5 часа от 8:30 до 17:30."""
    times = []
    start = time(8, 30)
    end = time(17, 30)
    current = start
    while current <= end:
        times.append((current.strftime("%H:%M"), current.strftime("%H:%M")))
        hours, minutes = divmod(current.minute + 90, 60)  # Шаг в 1.5 часа
        current = current.replace(hour=(current.hour + hours) % 24, minute=minutes)
    return times

def generate_stands_choices():
    """Генерирует список целых чисел от 1 до 4."""
    stands = []
    for i in range(1, 5):  # Генерируем числа от 1 до 4
        stands.append(i)
    return stands


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ["login", "password"]
        widgets = {"login": TextInput(attrs={
            "class": "form-control",
            "placeholder": "Login",
        }),
            "password": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Login",
        }),
        }

class TaskForm(ModelForm):
    name = forms.ChoiceField(label="Имя пользователя")  # Динамически наполняем в представлении
    time = forms.ChoiceField(label="Время", choices=generate_time_choices())  # Предопределенные временные слоты
    stand = forms.ChoiceField(label="Стенд", choices=[(i, str(i)) for i in range(1, 6)])  # Предопределенные временные слоты

    class Meta:
        model = Tasks
        fields = ["name", "time", "stand", "work_type"]
        widgets = {

            "work_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите тип работы"
            }),
        }




