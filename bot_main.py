# -*- coding: utf-8 -*-
import telebot
import config
import cherrypy
import inf
import psycopg2
from telebot import types

WEBHOOK_HOST = '185.228.233.139'
WEBHOOK_PORT = 88
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './certs/webhook_cert.pem'
WEBHOOK_SSL_PRIV = './certs/webhook_pkey.pem'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.token

bot = telebot.TeleBot(config.token)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


'''@bot.message_handler(func=lambda message: True, commands=['start'])
def select_user(message):
    if message.chat.username == 'den7i' or 'timurkorobov':
        admin_menu(message)

    elif None:
        main_menu(message)'''


def admin_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Начать диалог')
    keyboard.add('Получить последние 3 записи')
    keyboard.add('Получить последние 5 записей')
    msg = bot.send_message(message.chat.id, 'Админка', reply_markup=keyboard)
    bot.register_next_step_handler(msg, admin_select)


def admin_select(message):
    if message.text == 'Начать диалог':
        admin_menu(message)

    elif message.text == 'Получить последние 3 записи':
        admin_menu(message)

    elif message.text == 'Получить последние 5 записей':
        admin_menu(message)


@bot.message_handler(func=lambda message: True, commands=['start'])
def main_menu(message):
    config.excount = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📝 Заказать', '🥂 Банкет')
    keyboard.row('💰 Прайс-лист', 'ℹ Информация')
    if message.chat.username == 'den7i' or 'timurkorobov':
        admin_menu(message)
    msg = bot.send_message(message.chat.id, '📖 Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)


def menu(message):
    if message.text == '📝 Заказать':
        config.excount += 1
        order_tobacco(message)

    elif message.text == '🥂 Банкет':
        config.excount += 100
        banquet(message)

    elif message.text == '💰 Прайс-лист':
        price_list(message)

    elif message.text == 'ℹ Информация':
        info(message)


def order_tobacco(message):
    print(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🐒 Лёгкий', '🦍 Крепкий')
    msg = bot.send_message(message.chat.id, 'Выберите крепкость кальяна:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_tobacco_get)


def order_tobacco_get(message):
    if message.text == '🐒 Лёгкий':
        config.excount += 1
        order_cups(message)

    elif message.text == '🦍 Крепкий':
        config.excount += 10
        order_cups(message)


def order_cups(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('1️⃣ Одна', '2️⃣ Две', '3️⃣ Три')
    keyboard.row('🔢 Более трёх', '↪ Назад')
    msg = bot.send_message(message.chat.id, '☕ Выберите количество чашек:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_cups_get)


def order_cups_get(message):
    if message.text == '1️⃣ Одна':
        config.excount += 1
        order_set_address(message)

    elif message.text == '2️⃣ Две':
        config.excount += 2
        order_set_address(message)

    elif message.text == '3️⃣ Три':
        config.excount += 3
        order_set_address(message)

    elif message.text == '🔢 Более трёх':
        config.excount += 4
        order_set_address(message)

    elif message.text == '↪ Назад':
        order_tobacco(message)


def order_set_address(message):
    msg = bot.send_message(message.chat.id, 'Напишите адрес доставки')
    bot.register_next_step_handler(msg, verify_order)


def verify_order(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('✅ Да', '♻ Вернуться')
    msg = bot.send_message(message.chat.id, 'Подтвердите Ваш заказ\nВсе верно?', reply_markup=keyboard)
    config.address = message.text
    bot.register_next_step_handler(msg, yes_or_no)


def yes_or_no(message):
    if message.text == '✅ Да':
        done(message)

    elif message.text == '♻ Вернуться':
        order_set_address(message)


def done(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('✔ Завершить')
    msg = bot.send_message(message.chat.id, '📦 Заказ принят', reply_markup=keyboard)
    bot.register_next_step_handler(msg, close_order)


def db_update(message):
    conn = psycopg2.connect(database="testdb", user="postgres", password="12qwaszx", host="185.228.233.139",
                            port="5432")
    print('Connected to database')
    cur = conn.cursor()

    cur.execute('''INSERT INTO "USER_DATA" 
    VALUES (%s, %s, %s, 'Пользователь: %s\nЗаказ:\nЛёгкий кальян\n1 чаша\nАдрес: %s');''',
                (message.chat.id, message.chat.username, message.date, message.chat.id, inf.address))
    conn.commit()
    conn.close()


def db_get(message):
    conn = psycopg2.connect(database="testdb", user="postgres", password="12qwaszx", host="185.228.233.139",
                            port="5432")
    print('Connected to database')
    cur = conn.cursor()

    cur.execute('''SELECT ORDER from "USER_DATA" WHERE USER_ID=s%''', message.chat.id)
    user = cur.fetchone()
    bot.send_message(chat_id=config.my_id, text=user)
    conn.close()


def close_order(message):
    if message.text == '✔ Завершить':
        if config.excount == 3:
            db_update(message)

        elif config.excount == 4:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\n2 чаши\nПо адресу:\n' + inf.address)

        elif config.excount == 5:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\n3 чаши\nПо адресу:\n' + inf.address)

        elif config.excount == 6:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\nБолее трёх чаш\nПо адресу:\n' + inf.address)

        elif config.excount == 11:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n1 чаша\nПо адресу:\n' + inf.address)

        elif config.excount == 12:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n2 чаши\nПо адресу:\n' + inf.address)

        elif config.excount == 13:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n3 чаши\nПо адресу:\n' + inf.address)

        elif config.excount == 14:
            bot.send_message(chat_id=config.my_id,
                             text='Заказ:\nКрепкий кальян\nБолее трёх чаш\nПо адресу:\n' + inf.address)

        elif config.excount == 120:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nБанкет\nДо 5 человек\nПо адресу:\n' + inf.address)

        elif config.excount == 121:
            bot.send_message(chat_id=config.my_id,
                             text='Заказ:\nКрепкий кальян\nБолее 5 человек\nПо адресу:\n' + inf.address)

        elif config.excount == 122:
            bot.send_message(chat_id=config.my_id,
                             text='Заказ:\nКрепкий кальян\nБолее 10 человек\nПо адресу:\n' + inf.address)
    main_menu(message)


def banquet(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('До 5', '5+', '10+')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Сколько Вас человек?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, banquet_get)


def banquet_get(message):
    if message.text == 'До 5':
        config.excount += 10
        count_of_hookahs(message)

    elif message.text == '5+':
        config.excount += 11
        count_of_hookahs(message)

    elif message.text == '10+':
        config.excount += 12
        count_of_hookahs(message)

    elif message.text == '↪ Назад':
        main_menu(message)


def count_of_hookahs(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Один', 'Два', 'Три')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Сколько нужно кальянов?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, count_of_hookahs_get)


def count_of_hookahs_get(message):
    if message.text == 'Один':
        config.excount += 10
        order_set_address(message)

    elif message.text == 'Два':
        config.excount += 10
        order_set_address(message)

    elif message.text == 'Три':
        config.excount += 10
        order_set_address(message)

    elif message.text == '↪ Назад':
        banquet(message)


def price_list(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Табак', 'Обслуживание банкетов')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Прайс-лист:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, price_list_get)


def price_list_get(message):
    if message.text == 'Табак':
        tobacco_prices(message)

    elif message.text == 'Обслуживание банкетов':
        bot.send_message(message.chat.id, inf.banquet_price)
        price_list(message)

    elif message.text == '↪ Назад':
        main_menu(message)


def tobacco_prices(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Лёгкий', 'Крепкий')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Табак:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, tobacco_prices_get)


def tobacco_prices_get(message):
    if message.text == 'Лёгкий':
        bot.send_message(message.chat.id, inf.easy_tobacco)
        price_list(message)

    elif message.text == 'Крепкий':
        bot.send_message(message.chat.id, inf.hard_tobacco)
        price_list(message)

    elif message.text == '↪ Назад':
        main_menu(message)


def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Правила предоставления услуг')
    keyboard.row('Штрафы', 'О нас')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Информация:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, select_info)


def select_info(message):
    if message.text == 'Правила предоставления услуг':
        bot.send_message(message.chat.id, 'Empty')
        info(message)

    elif message.text == 'Штрафы':
        bot.send_message(message.chat.id, 'Empty')
        info(message)

    elif message.text == 'О нас':
        bot.send_message(message.chat.id, 'Empty')
        info(message)

    elif message.text == '↪ Назад':
        main_menu(message)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})


if __name__ == '__main__':
    bot.polling(none_stop=True)
