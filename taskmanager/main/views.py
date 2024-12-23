from django.shortcuts import render, redirect, get_object_or_404

from .forms import UsersForm, TaskForm
from .models import Users, Tasks
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import timedelta, datetime
import psycopg2
from psycopg2 import sql, connect
from datetime import timedelta, datetime
from django.db import connections
import threading
import time

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

@login_required
def list_reg(request):
    user = request.user
    form = TaskForm()  # Создаем экземпляр формы для отображения
    form.fields['name'].choices = [(user.username, user.username)]
    form.fields['stand'].choices = [(i, str(i)) for i in range(1, 6)]

    if request.method == 'POST':
        form = TaskForm(request.POST)  # Получаем данные из формы
        form.fields['name'].choices = [(user.username, user.username)]
        form.fields['stand'].choices = [(i, str(i)) for i in range(1, 6)]

        if form.is_valid():
            name = form.cleaned_data.get('name')
            time_str = form.cleaned_data.get('time')
            stand = form.cleaned_data.get('stand')
            work_type = form.cleaned_data.get('work_type')

            try:
                # Получаем последнюю запись по времени
                time_obj = datetime.strptime(time_str, "%H:%M").time()
                ##last_task = Tasks.objects.using('secondary').order_by('-time').first()
                existing_task = Tasks.objects.using('secondary').filter(time=time_obj, stand=stand).first()

                if existing_task:
                    return render(request, 'main/list_reg.html', {
                        'form': form,
                        'error': f'Запись с таким временем {time_str} и стендом {stand} уже существует.'
                    })
                conflicting_tasks = Tasks.objects.using('secondary').filter(time=time_obj).exclude(stand=stand)
                for last_task in conflicting_tasks:
                    time_difference = datetime.combine(datetime.today(), time_obj) - datetime.combine(datetime.today(),
                                                                                                      last_task.time)
                # Если есть предыдущая запись, проверяем разницу во времени
               ## if last_task:
                    # Рассчитываем разницу во времени между новой записью и последней
                 ##   time_difference = datetime.combine(datetime.today(), time_obj) - datetime.combine(datetime.today(),
                                                                                                    ##  last_task.time)
                    # Если разница меньше 1.5 часов, возвращаем ошибку
                   ## if time_difference < timedelta(hours=1, minutes=30) :
                   ##     return render(request, 'main/list_reg.html', {
                    ##        'form': form,
                    ##        'error': 'Разница во времени между записями должна составлять минимум 1.5 часа.'
                     ##   })

                # Сохраняем данные во вторую базу данных
                Tasks.objects.using('secondary').create(
                    name=name,
                    time=time_obj,
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


def update_stand_status_forever():
    while True:
        try:
            # Текущее время
            now = datetime.now()

            # Используем вторичную базу данных
            with connections['secondary'].cursor() as cursor:
                # Установить статус None, если разница во времени (включая дату) больше 5 минут
                cursor.execute("""
                    UPDATE stand 
                    SET status = %s 
                    WHERE time < %s
                """, ['занят', now - timedelta(minutes=5)])
                cursor.execute("""
                                    UPDATE stand 
                                    SET status = %s 
                                    WHERE time > %s
                                """, ['свободен', now - timedelta(minutes=5)])
                if cursor.rowcount > 0:
                    print(f"Обновлено {cursor.rowcount} строк(и).")
        except Exception as e:
            print(f"Ошибка при работе с базой данных: {e}")

        # Интервал между выполнениями (например, каждые 5 секунд)
        time.sleep(5)



        # Перенаправляем на другую страницу после обновления

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