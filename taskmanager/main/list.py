import psycopg2
import cgi
import cgitb

# Для отладки (включить вывод ошибок CGI в браузер)
cgitb.enable()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="list",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

# Создание таблицы
with conn:
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS my_table_1 (
                name TEXT,
                time TEXT,
                stand TEXT,
                work_type TEXT
            );
        """)

# Получение данных из формы
form = cgi.FieldStorage()
name = form.getvalue("name")
time = form.getvalue("time")
stand = form.getvalue("stand")
work_type = form.getvalue("work_type")

# Проверка, что данные получены корректно
if name and time and stand and work_type:
    try:
        # Вставка данных в таблицу
        with conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO my_table_1 (name, time, stand, work_type)
                VALUES (%s, %s, %s, %s);
                """
                cursor.execute(query, (name, time, stand, work_type))

        # Успешное добавление
        print("Content-Type: text/html\n")
        print("<html><body><h2>Данные успешно добавлены!</h2></body></html>")

    except Exception as e:
        # Обработка ошибок
        print("Content-Type: text/html\n")
        print(f"<html><body><h2>Ошибка при добавлении данных: {e}</h2></body></html>")

else:
    print("Content-Type: text/html\n")
    print("<html><body><h2>Пожалуйста, заполните все поля формы.</h2></body></html>")

# Закрытие соединения
conn.close()
