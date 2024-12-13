from .models import Users, Tasks
from django.forms import ModelForm, TextInput, Textarea



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
    class Meta:
        model = Tasks
        fields = ["name", "time", "stand", "work_type"]
        widgets = {
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название задачи",
            }),
            "time": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Выберите время",
            }),
            "stand": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Выберите стенд",
            }),
            "work_type": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Выберите тип работы",
            }),
        }