# -*- coding: utf-8 -*-
import telebot
import config
import inf
from telebot import types
# import psycopg2

bot = telebot.TeleBot(config.token)
# conn = psycopg2.connect(database="testdb", user="admin", password="12qwaszx", host="127.0.0.1", port="5432")
# print('Connected')
# cur = conn.cursor()


@bot.message_handler(commands=['start'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📝 Заказать', '🥂 Корпоратив')
    keyboard.row('💰 Прайс-лист', '⚙ Настройки')
    keyboard.row('ℹ Информация', '👔 О нас')
    msg = bot.send_message(message.chat.id, '📖 Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)


def menu(message):
    print(message)
    if message.text == '📝 Заказать':
        order_tobacco(message)

    elif message.text == '🥂 Банкет':
        pass

    elif message.text == '💰 Прайс-лист':
        price_list(message)

    elif message.text == '⚙ Настройки':
        settings(message)

    elif message.text == 'ℹ Информация':
        info(message)

    elif message.text == '👔 О нас':
        about(message)


def order_tobacco(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🐒 Лёгкий', '🦍 Крепкий')
    msg = bot.send_message(message.chat.id, 'Выберите крепкость кальяна:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_tobacco_get)


def order_tobacco_get(message):
    if message.text == '🐒 Лёгкий':
        order_cups(message)

    elif message.text == '🦍 Крепкий':
        order_cups(message)


def order_cups(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('1️⃣ Одна', '2️⃣ Две', '3️⃣ Три')
    keyboard.row('🔢 Более трёх', '↪ Назад')
    msg = bot.send_message(message.chat.id, '☕ Выберите количество чашек:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_cups_get)


def order_cups_get(message):
    if message.text == '1️⃣ Одна':
        order_set_address_get(message)

    elif message.text == '2️⃣ Две':
        order_set_address_get(message)

    elif message.text == '3️⃣ Три':
        order_set_address_get(message)

    elif message.text == '🔢 Более трёх':
        order_set_address_get(message)

    elif message.text == '↪ Назад':
        order_tobacco(message)


def order_set_address_get(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    geolocation_button = types.KeyboardButton(text="📍 Местоположение", request_location=True)
    keyboard.add(geolocation_button)
    msg = bot.send_message(message.chat.id, 'Напишите адрес доставки\nИли отправьте местоположение',
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, address_or_location)


def address_or_location(message):
    print(message.text)
    if message.text != '📍 Местоположение':
        verify_order(message)


def verify_order(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('✅ Да', '♻ Вернуться')
    msg = bot.send_message(message.chat.id, 'Подтвердите Ваш заказ\nВсе верно?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, yes_or_no)


def yes_or_no(message):
    if message.text == '✅ Да':
        done(message)

    elif message.text == '♻ Вернуться':
        order_set_address_get(message)


def done(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('✔ Завершить')
    msg = bot.send_message(message.chat.id, '📦 Заказ принят', reply_markup=keyboard)
    bot.register_next_step_handler(msg, close_order)


def close_order(message):
    if message.text == '✔ Завершить':
        main_menu(message)


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


def tobacco_prices(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Лёгкий', 'Крепкий')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Табак:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, tobacco_prices)


def tobacco_prices_get(message):
    if message.text == 'Лёгкий':
        bot.send_message(message.chat.id, inf.easy_tobacco)

    elif message.text == 'Крепкий':
        bot.send_message(message.chat.id, inf.hard_tobacco)


def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🏠 Домашний адрес', '📚 История заказов')
    keyboard.row('📢 Поделиться ботом', '↪ Назад')
    msg = bot.send_message(message.chat.id, '👤 Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)


def account_info(message):
    if message.text == '🏠 Домашний адрес':
        pass

    elif message.text == '📚 История заказов':
        pass

    elif message.text == '📢 Поделиться ботом':
        pass

    elif message.text == '↪ Назад':
        main_menu(message)


def about(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    msg = bot.send_message(message.chat.id, inf.about_us, reply_markup=keyboard)
    bot.register_next_step_handler(msg, main_menu)

def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    msg = bot.send_message(message.chat.id, inf.info_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, main_menu)

def order_done(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('📖 Главное меню')
    msg = bot.send_message(message.chat.id, 'Заказ принят', reply_markup=keyboard)
    bot.register_next_step_handler(msg, main_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
