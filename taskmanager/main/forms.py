from .models import Users
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