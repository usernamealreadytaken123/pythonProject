from django.shortcuts import render, redirect, get_object_or_404

from .forms import UsersForm, TaskForm
from .models import Users, Tasks
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import psycopg2


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

def list_reg(request):
    form = TaskForm()  # Создаем экземпляр формы для отображения

    if request.method == 'POST':
        form = TaskForm(request.POST)  # Получаем данные из формы
        if form.is_valid():
            name = form.cleaned_data.get('name')
            time = form.cleaned_data.get('time')
            stand = form.cleaned_data.get('stand')
            work_type = form.cleaned_data.get('work_type')

            try:
                # Сохраняем данные во вторую базу данных
                Tasks.objects.using('secondary').create(
                    name=name,
                    time=time,
                    stand=stand,
                    work_type=work_type
                )
                # Возвращаем успешный ответ
                return render(request, 'main/list_reg.html', {
                    'form': TaskForm(),  # Обнуляем форму после успешного добавления
                    'success': 'Данные успешно добавлены во вторую базу данных!'
                })
            except Exception as e:
                # Возвращаем ошибку при добавлении
                return render(request, 'main/list_reg.html', {
                    'form': form,
                    'error': f"Ошибка при добавлении данных: {e}"
                })

    # Если GET-запрос, просто отображаем форму
    return render(request, 'main/list_reg.html', {'form': form})





def tasks_list(request):
    # Получаем все записи из таблицы Tasks
    tasks = Tasks.objects.using('secondary').all()

    # Передаем записи в шаблон
    return render(request, 'main/tasks_list.html', {'tasks': tasks})



'''def list_reg(request):
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get("name")
        time = request.POST.get("time")
        stand = request.POST.get("stand")
        work_type = request.POST.get("work_type")

        # Подключение к базе данных
        conn = psycopg2.connect(
            dbname="list",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )

        try:
            with conn:
                with conn.cursor() as cursor:
                    # SQL-запрос для вставки данных
                    query = """
                        INSERT INTO my_table_1 (name, time, stand, work_type)
                        VALUES (%s, %s, %s, %s);
                        """
                    cursor.execute(query, (name, time, stand, work_type))

            return HttpResponse("<h2>Данные успешно добавлены!</h2>")
        except Exception as e:
            return HttpResponse(f"<h2>Ошибка при добавлении данных: {e}</h2>")
        finally:
            conn.close()

    return render(request, 'main/list_reg.html')  # Если GET-запрос, просто отображаем форму"'''