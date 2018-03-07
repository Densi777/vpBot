# -*- coding: utf-8 -*-
import telebot
#import psycopg2
import config
import inf
from telebot import types
import datetime

bot = telebot.TeleBot(config.token)
#conn = psycopg2.connect( host='localhost', user=den, password=root7, dbname=vpbot_accounts_db)
#cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def mainMenu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📝 Заказать', '🥂 Корпоратив')
    keyboard.row('💰 Прайс-лист', '⚙ Настройки')
    keyboard.row('ℹ Информация', '👔 О нас')
    msg = bot.send_message(message.chat.id, '📖 Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)

def menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == '📝 Заказать':
        order_tobacco(message)

    elif message.text == '🥂 Корпоратив':
        party(message)

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
    bot.register_next_step_handler(msg, order_cups_get)

def order_cups_get(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('1️⃣ Одна', '2️⃣ Две', '3️⃣ Три')
    keyboard.row('🔢 Более трёх', '↪ Назад')
    msg = bot.send_message(message.chat.id, '☕ Выберите количество чашек:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_cups)

def order_cups(message):
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

@bot.message_handler(commands=['geophone'])
def order_set_address_get(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    geolocation_button = types.KeyboardButton(text="📍 Местоположение", request_location=True)
    keyboard.add(geolocation_button, '↪ Назад')
    bot.send_message(message.chat.id, 'Напишите адрес доставки\nИли отправьте местоположение', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_set_address)

@bot.message_handler(commands=['geophone'])
def order_set_address(message):
    if keyboard == geolocation_button:
        bot.send_location(location.chat.id, 'Местоположение отправлено')

    elif message.text == '↪ Назад':
        order_cups_get(message)

def price_list(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🐒 Лёгкий', '🦍 Крепкий')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, 'Выберите крепкость кальяна:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, tobaccos_prices)

def tobaccos_prices(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    if message.text == '🐒 Лёгкий':
        msg = bot.send_message(message.chat.id, inf.easy_tobacco, reply_markup=keyboard)

    elif message.text == '🦍 Крепкий':
        msg = bot.send_message(message.chat.id, inf.hard_tobacco, reply_markup=keyboard)

    elif message.text == '↪ Назад':
        mainMenu(message)

def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🏠 Домашний адрес', '📚 История заказов')
    keyboard.row('📢 Поделиться ботом' ,'↪ Назад')
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
        mainMenu(message)


def about(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    msg = bot.send_message(message.chat.id, inf.about_us, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)

def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    msg = bot.send_message(message.chat.id, inf.info_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)

@bot.message_handler(commands=['geophone'])
def geophone(message):
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)


if __name__ == '__main__':
    bot.polling(none_stop=True)
