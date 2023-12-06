import numpy as numpy  # импорт библиотек для работы бота
import telebot
import pymysql
from telebot import types

print("Загрузка бота...")
bot = telebot.TeleBot('6792924162:AAHKgpSjb_7_wV799VokWAUM5gVGlRNUWN4')  # подключение к боту

status = {}


def get_audience_info(message_chat_id):  # функция, обрабатывающая информацию об аудиториях
    try:
        connection = pymysql.connect(
            host='FVH1.spaceweb.ru',
            user='vadzaharki',
            password='Kinimi256891',
            db='vadzaharki'
        )
        with connection.cursor() as cursor:
            select_id_univ = "SELECT ID FROM universities_buildings where Name = '" + status[message_chat_id][1] + "'"
            cursor.execute(select_id_univ)
            rows = cursor.fetchall()
            select_audience_info = "SELECT * FROM audiences WHERE ID_B = " + str(rows[0][0]) + " AND Number = " + \
                                   status[message_chat_id][2]
            cursor.execute(select_audience_info)
            rows = cursor.fetchall()
        connection.close()
        if rows[0] == ():
            return "error"
        return rows
    except Exception as ex:
        print(ex)
        return "error"


def get_list_univ():  # функция, обрабатывающая информацию об университетах
    try:
        connection = pymysql.connect(
            host='FVH1.spaceweb.ru',
            user='vadzaharki',
            password='Kinimi256891',
            db='vadzaharki'
        )
        with connection.cursor() as cursor:
            select_all_univ = "SELECT Name FROM universities"
            cursor.execute(select_all_univ)
            rows = cursor.fetchall()
        connection.close()
    except Exception as ex:
        print(ex)
    return rows


def get_list_build(univ):  # функция, обрабатывающая информацию о корпусах университетов
    try:
        connection = pymysql.connect(
            host='FVH1.spaceweb.ru',
            user='vadzaharki',
            password='Kinimi256891',
            db='vadzaharki'
        )
        with connection.cursor() as cursor:
            select_id_univ = "SELECT ID FROM universities where Name = '" + univ + "'"
            cursor.execute(select_id_univ)
            rows = cursor.fetchall()
            select_list_build = "SELECT Name FROM universities_buildings WHERE ID_U = " + str(rows[0][0])
            cursor.execute(select_list_build)
            row = cursor.fetchall()
        connection.close()
    except Exception as ex:
        print(ex)
    return row


def get_all_list_build():  # функция, обрабатывающая информацию об унивенрситетах
    try:
        connection = pymysql.connect(
            host='FVH1.spaceweb.ru',
            user='vadzaharki',
            password='Kinimi256891',
            db='vadzaharki'
        )
        with connection.cursor() as cursor:
            select_list_build = "SELECT Name FROM universities_buildings"
            cursor.execute(select_list_build)
            row = cursor.fetchall()
        connection.close()
    except Exception as ex:
        print(ex)
    return row


@bot.message_handler(commands=['start'])  # запуск бота, вывод вариантов на выбор для первого этапа работы программы
def start_message(message):
    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("До аудитории")
        btn2 = types.KeyboardButton("Авторы")
        btn3 = types.KeyboardButton("До общежития")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text="Привет! Я бот, который поможет тебе найти аудиторию в КНИТУ! ".format(
                             message.from_user), reply_markup=markup)


@bot.message_handler(
    content_types=['text'])  # переход на второй этап работы программы, обработка полученных данных, переход далее
def message_reply(message):
    if message.chat.id not in status:
        status[message.chat.id] = ["", "", ""]
    if message.text == "Авторы":
        bot.send_message(message.chat.id, "Бот сделан V и N")
    if message.text == "До аудитории":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        univs = get_list_univ()
        for i in range(len(univs)):
            univ = "".join(univs[i])
            item1 = types.KeyboardButton(univ)
            markup.add(item1)
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("На главную"))
        bot.send_message(message.chat.id, "Выберите нужный вуз".format(message.from_user), reply_markup=markup)

    if message.text == "До общежития":
        bot.send_message(message.chat.id,
                         "от общежития до корпусов университета и обратно можно добраться следующим образом:\n 1)корпус Д - автобусы 1,4,25 с остановки ""ул.Вишневского"" до остановки ""ул.Пионерская""\n 2)корпус А - автобусы 22,30,89 с остановки ""ул.Товарищеская"" до остановки ""ул.Толстова"" ")

    if message.text == "На главную":
        status[message.chat.id][0] = ""
        status[message.chat.id][1] = ""
        status[message.chat.id][2] = ""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("До аудитории")
        btn2 = types.KeyboardButton("Авторы")
        btn3 = types.KeyboardButton("До общежития")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text="Привет! Я бот, который поможет тебе найти аудиторию в КНИТУ! ".format(
                             message.from_user), reply_markup=markup)
    if message.text == "Назад":
        if status[message.chat.id][0] == "":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("До аудитории")
            btn2 = types.KeyboardButton("Авторы")
            btn3 = types.KeyboardButton("До общежития")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id,
                             text="Привет! Я бот, который поможет тебе найти аудиторию в КНИТУ! ".format(
                                 message.from_user), reply_markup=markup)
        elif status[message.chat.id][1] == "":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            univs = get_list_univ()
            for i in range(len(univs)):
                univ = "".join(univs[i])
                item1 = types.KeyboardButton(univ)
                markup.add(item1)
            markup.add(types.KeyboardButton("Назад"))
            markup.add(types.KeyboardButton("На главную"))
            bot.send_message(message.chat.id, "Выберите нужный вуз".format(message.from_user), reply_markup=markup)
        elif status[message.chat.id][2] == "":
            status[message.chat.id][1] = ""
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            builds = get_list_build(status[message.chat.id][0])
            for i in range(len(builds)):
                build = "".join(builds[i])
                item1 = types.KeyboardButton(build)
                markup.add(item1)
            markup.add(types.KeyboardButton("Назад"))
            markup.add(types.KeyboardButton("На главную"))
            bot.send_message(message.chat.id, "Выберите нужный корпус".format(message.from_user), reply_markup=markup)


    elif message.text in numpy.hstack(get_list_univ()).tolist():
        status[message.chat.id][0] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        builds = get_list_build(status[message.chat.id][0])
        for i in range(len(builds)):
            build = "".join(builds[i])
            item1 = types.KeyboardButton(build)
            markup.add(item1)
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("На главную"))
        bot.send_message(message.chat.id, "Выберите нужный корпус".format(message.from_user), reply_markup=markup)

    elif status[message.chat.id][0] != "" and status[message.chat.id][1] != "":
        status[message.chat.id][2] = message.text
        info = get_audience_info(message.chat.id)
        if info == "error":
            bot.send_message(message.chat.id,
                             "Такой аудитории не существует/мы ее еще не добавили ^_^".format(message.from_user))
        else:
            contex = info[0][3]
            picture_path = info[0][4]
            bot.send_photo(message.chat.id, picture_path, caption=contex)

    elif status[message.chat.id][0] != "":
        status[message.chat.id][1] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("На главную"))
        bot.send_message(message.chat.id, "Введите нужную аудиторию".format(message.from_user), reply_markup=markup)


bot.infinity_polling()
