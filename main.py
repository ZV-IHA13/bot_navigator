import numpy as numpy
import telebot
import pymysql
from telebot import types

print("Загрузка бота...")
bot = telebot.TeleBot('6792924162:AAHKgpSjb_7_wV799VokWAUM5gVGlRNUWN4')

status = ["", "", ""]


def get_audience_info():
    try:
        connection = pymysql.connect(
            host='FVH1.spaceweb.ru',
            user='vadzaharki',
            password='Kinimi256891',
            db='vadzaharki'
        )
        with connection.cursor() as cursor:
            select_id_univ = "SELECT ID FROM universities_buildings where Name = '" + status[1] + "'"
            cursor.execute(select_id_univ)
            rows = cursor.fetchall()
            select_audience_info = "SELECT * FROM audiences WHERE ID_B = " + str(rows[0][0]) + " AND Number = " + \
                                   status[2]
            cursor.execute(select_audience_info)
            rows = cursor.fetchall()
        connection.close()
        if rows[0] == ():
            return "error"
        return rows
    except Exception as ex:
        print(ex)
        return "error"


def get_list_univ():
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


def get_list_build(univ):
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


def get_all_list_build():
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


@bot.message_handler(commands=['start'])
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


@bot.message_handler(content_types=['text'])
def message_reply(message):
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
        bot.send_message(message.chat.id, "тут что то будет")

    if message.text == "На главную":
        status[0] = ""
        status[1] = ""
        status[2] = ""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("До аудитории")
        btn2 = types.KeyboardButton("Авторы")
        btn3 = types.KeyboardButton("До общежития")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text="Привет! Я бот, который поможет тебе найти аудиторию в КНИТУ! ".format(
                             message.from_user), reply_markup=markup)
    if message.text == "Назад":
        if status[0] == "":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("До аудитории")
            btn2 = types.KeyboardButton("Авторы")
            btn3 = types.KeyboardButton("До общежития")
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.chat.id,
                             text="Привет! Я бот, который поможет тебе найти аудиторию в КНИТУ! ".format(
                                 message.from_user), reply_markup=markup)
        elif status[1] == "":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            univs = get_list_univ()
            for i in range(len(univs)):
                univ = "".join(univs[i])
                item1 = types.KeyboardButton(univ)
                markup.add(item1)
            markup.add(types.KeyboardButton("Назад"))
            markup.add(types.KeyboardButton("На главную"))
            bot.send_message(message.chat.id, "Выберите нужный вуз".format(message.from_user), reply_markup=markup)
        elif status[2] == "":
            status[1] = ""
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            builds = get_list_build(status[0])
            for i in range(len(builds)):
                build = "".join(builds[i])
                item1 = types.KeyboardButton(build)
                markup.add(item1)
            markup.add(types.KeyboardButton("Назад"))
            markup.add(types.KeyboardButton("На главную"))
            bot.send_message(message.chat.id, "Выберите нужный корпус".format(message.from_user), reply_markup=markup)


    elif message.text in numpy.hstack(get_list_univ()).tolist():
        status[0] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        builds = get_list_build(status[0])
        for i in range(len(builds)):
            build = "".join(builds[i])
            item1 = types.KeyboardButton(build)
            markup.add(item1)
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("На главную"))
        bot.send_message(message.chat.id, "Выберите нужный корпус".format(message.from_user), reply_markup=markup)

    elif status[0] != "" and status[1] != "":
        status[2] = message.text
        info = get_audience_info()
        if info == "error":
            bot.send_message(message.chat.id, "Такой аудитории не существует/мы ее еще не добавили ^_^".format(message.from_user))
        else:
            contex = info[0][3]
            picture_path = info[0][4]
            bot.send_photo(message.chat.id, picture_path, caption=contex)

    elif status[0] != "":
        status[1] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Назад"))
        markup.add(types.KeyboardButton("На главную"))
        bot.send_message(message.chat.id, "Введите нужную аудиторию".format(message.from_user), reply_markup=markup)


bot.infinity_polling()
