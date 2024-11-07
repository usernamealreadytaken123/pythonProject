import psycopg2
import telebot
from telebot import types

# Establish connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

    if conn.closed:
        print("Соединение с базой данных закрыто.")
    else:
        print("Соединение с базой данных открыто.")
    conn.close()
except psycopg2.Error as e:
    print("Ошибка подключения к базе данных:", e)

# Establish connection to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15 FROM my_table_0")
    rows = cur.fetchall()

    if rows:
        print("Значения переменных из базы данных:")
        for row in rows:
            print(row)
    else:
        print("В таблице нет данных.")

    cur.close()
    conn.close()
except psycopg2.Error as e:
    print("Ошибка при доступе к базе данных:", e)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Create a table with boolean variables
cur.execute("""
    CREATE TABLE IF NOT EXISTS my_table_0 (
        var1 BOOLEAN DEFAULT TRUE,
        var2 BOOLEAN DEFAULT TRUE,
        var3 BOOLEAN DEFAULT TRUE,
        var4 BOOLEAN DEFAULT TRUE,
        var5 BOOLEAN DEFAULT TRUE,
        var6 BOOLEAN DEFAULT TRUE,
        var7 BOOLEAN DEFAULT TRUE,
        var8 BOOLEAN DEFAULT TRUE,
        var9 BOOLEAN DEFAULT TRUE
    );
""")

conn.commit()
cur.execute("""
    CREATE TABLE IF NOT EXISTS my_table_inf_0 (
    str1 VARCHAR(255),
    str2 VARCHAR(255),
    str3 VARCHAR(255),
    str4 VARCHAR(255),
    str5 VARCHAR(255),
    str6 VARCHAR(255),
    str7 VARCHAR(255),
    str8 VARCHAR(255),
    str9 VARCHAR(255)
    );
""")
conn.commit()
# Close the cursor
cur.close()

# Initialize the Telegram bot
bot = telebot.TeleBot('6743095111:AAGX1CK82sdKOdUQR8W4UUXYqfRUSW5Sp08')
user_states = {}


# Function to get variable statuses from the database



# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    user_states[message.chat.id] = 'awaiting_password'
    bot.send_message(message.chat.id, 'Введите пароль:')


# Handler for entering the password
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'awaiting_password')
def check_password(message):
    if message.text.strip() == '123':
        user_states[message.chat.id] = 'authenticated'
        # Send the menu to the user after successful authentication
        send_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль. Попробуйте еще раз.')





# Function to send the menu
def send_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton('Узнать свое имя'),
               types.KeyboardButton('Узнать свой id'),
               types.KeyboardButton('Забронировать стол'))
    bot.send_message(chat_id, 'Меню доступных команд:', reply_markup=markup)



# Handler for the /name command
@bot.message_handler(func=lambda message: message.text == 'Узнать свое имя')
def info_name(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name}")


# Handler for the /id command
@bot.message_handler(func=lambda message: message.text == 'Узнать свой id')
def info_id(message):
    bot.send_message(message.chat.id, f'ID:{message.from_user.id} ')




# Function to get variable statuses from the database
def get_var_statuses(day_number):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    print(day_number)
    cur = conn.cursor()
    cur.execute(f"SELECT var1, var2, var3, var4, var5, var6, var7, var8, var9 FROM my_table_{day_number}")

    row = cur.fetchone()
    print(row)
    print(row)
    print(row)
    print(row)
    conn.commit()
    cur.close()
    return row







# Handler for the /button command

def send_buttons(message,day_number):

    print('11', day_number)
    var_statuses = get_var_statuses(day_number)

    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []

    for i, var_status in enumerate(var_statuses[0:], start=1):
        color = '🟢 Свободно' if var_status else '🔴 Занят'
        button_text = f"Стол {i} {color}"
        button_callback_data = f"btn{i}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=button_callback_data)
        buttons.append(button)

    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выберите стол:", reply_markup=markup)






# Callback handler for button presses
var_num = None  # Объявляем переменную в глобальной области видимости
day_number = None
# Callback handler for button presses
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global var_num
    global day_number

    if call.data.startswith("calen"):
        day_number = int(call.data.split("_1")[-1])
        send_buttons(call.message, day_number)  # Pass day_number as an argument here
        print('33')

    if call.data == 'new_button_20':
        send_calendar(call.message)

    if call.data.startswith("btn"):

        print('22', day_number)
        var_num = int(call.data.replace("btn", ""))

        button_number = int(call.data[3:])  # Получаем номер кнопки из call.data
        var_statuses = get_var_statuses(day_number)
        if var_statuses[button_number - 1]:  # Проверяем статус переменной для данной кнопки
            send_additional_buttons(call.message)
        else:
            send_more_buttons(call.message)  # Если кнопка красная, вызываем функцию для красных кнопок
    elif call.data == 'new_button_1':  # Проверяем нажатие на кнопку "new_button_1"
        if var_num is not None:  # Проверяем, было ли установлено значение var_num
            update_var_status(var_num,day_number)
            bot.answer_callback_query(call.id, "стол забронирован")  # Отвечаем на колбэк
            reserve_table(call)

        else:
            bot.answer_callback_query(call.id, "Не удалось определить номер стола")  # Обработка ошибки
    elif call.data == 'new_button_3':  # Проверяем нажатие на кнопку "new_button_3"
        if var_num is not None:
            update_var_status(var_num, day_number)
            bot.answer_callback_query(call.id, "бронь снята")  # Отвечаем на колбэк
            send_more_buttons1(call.message)
    elif call.data == 'new_button_7':  # Проверяем нажатие на кнопку "new_button_7"
        if var_num is not None:
            show_reservation_info(call)
        else:
            bot.answer_callback_query(call.id, "Не удалось определить номер стола")
    elif call.data == 'new_button_5':
         send_buttons(call.message,day_number)
    else:
        if call.data == 'new_button_2':
            send_buttons(call.message,day_number)
        if call.data == 'new_button_4':
            send_buttons(call.message,day_number)





# Function to send additional buttons
def send_additional_buttons(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Забронировать стол", callback_data="new_button_1"),
               types.InlineKeyboardButton("Выбрать другой стол", callback_data="new_button_2"),
               types.InlineKeyboardButton("Выбрать другой день", callback_data="new_button_20"))
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

def send_more_buttons(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Снять бронь", callback_data="new_button_3"),
               types.InlineKeyboardButton("Выбрать другой стол", callback_data="new_button_4"),
               types.InlineKeyboardButton("Выбрать другой день", callback_data="new_button_20"),
               types.InlineKeyboardButton("Посмотреть информацию", callback_data="new_button_7"))
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

def send_more_buttons1(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Да", callback_data="new_button_5"),
               types.InlineKeyboardButton("Нет", callback_data="new_button_6"))
    bot.send_message(message.chat.id, "Хотите забронировать другой стол?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Забронировать стол')
def send_calendar(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(types.InlineKeyboardButton("День1", callback_data="calen_button_10"),
               types.InlineKeyboardButton("День2", callback_data="calen_button_11"),
               types.InlineKeyboardButton("День3", callback_data="calen_button_12"),
               types.InlineKeyboardButton("День4", callback_data="calen_button_13"),
               types.InlineKeyboardButton("День5", callback_data="calen_button_14"),
               types.InlineKeyboardButton("День6", callback_data="calen_button_15"),
               types.InlineKeyboardButton("День7", callback_data="calen_button_16"))
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=markup)

# Function to update the status of the variable in the database
def update_var_status(var_num,day_number):
    print(day_number)
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(f"UPDATE my_table_{day_number} SET var{var_num} = NOT var{var_num}")
    conn.commit()
    cur.close()

print(var_num)
# Функция сохранения информации о бронировании стола
def save_reservation_info(message):
    global var_num
    print(var_num)
    if var_num is not None:
        reservation_info = message.text.strip()

        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        try:
            cur.execute(f"UPDATE my_table_inf_{day_number} SET str{var_num} = '{reservation_info}'")
            conn.commit()
            cur.close()
            print(f"Значение переменной str{var_num}: {reservation_info}")

            bot.send_message(message.chat.id, "Информация о бронировании сохранена.")
            send_more_buttons1(message)
        except psycopg2.Error as e:
            print("Ошибка при выполнении запроса:", e)
            conn.rollback()  # Откат изменений в случае ошибки
            cur.close()
            bot.send_message(message.chat.id, "Произошла ошибка при сохранении информации.")
    else:
        bot.send_message(message.chat.id, "Не удалось определить номер стола. Попробуйте еще раз.")



# Обработчик нажатия кнопки "Забронировать стол"
def reserve_table(call):
    global var_num
    bot.send_message(call.message.chat.id, "Введите информацию для бронирования стола:")
    bot.register_next_step_handler(call.message, save_reservation_info)



try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(
          f"SELECT str1, str2, str3, str4, str5, str6, str7, str8, str9 FROM my_table_inf_{day_number}")
    rows = cur.fetchall()

    if rows:
        print("Значения переменных из базы данных:")
        for row in rows:
            print(row)
    else:
        print("В таблице нет данных.")

    cur.close()
    conn.close()
except psycopg2.Error as e:
    print("Ошибка при доступе к базе данных:", e)


def show_reservation_info(call):
    print(day_number, "wewe")
    print("Вызвана функция show_reservation_info")
    global var_num
    print(var_num)
    if var_num is None:
        bot.send_message(call.message.chat.id, "Не удалось определить номер стола")
        return

    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(f"SELECT str{var_num} FROM my_table_inf_{day_number}")
    row = cur.fetchone()
    conn.commit()
    cur.close()

    if row:
        bot.send_message(call.message.chat.id, f"Информация о бронировании: {row[0]}")
        print(row[0])
    else:
        bot.send_message(call.message.chat.id, "Информация о бронировании отсутствует.")








# Start the bot
bot.polling(none_stop=True)
