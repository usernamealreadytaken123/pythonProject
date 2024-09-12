from django.shortcuts import render, redirect, get_object_or_404

from .forms import UsersForm
from .models import Users
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



def index(request):
    users = Users.objects.all()
    return render(request, 'main/index.html',{'login': 'Главная страница сайта', 'users': users})

def about(request):
    return render(request, 'main/about.html')
def book(request):
    return render(request, 'main/book.html')


def profile(request):
    error = ''
    if request.method == 'POST':
        form = UsersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('about')
        else:
            error = 'error'

    form = UsersForm()
    context = {
        'form': form,
        'error': error
    }

    return render(request, 'main/profile.html', context)


def auth(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('about')
            else:
                error = 'Invalid username or password.'
    else:
        form = AuthenticationForm()
        error = None

    return render(request, 'main/auth.html', {'form': form, 'error': error})

@login_required
def about(request):
    return render(request, 'main/about.html')
