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
        pass

    elif message.text == '🥂 Корпоратив':
        pass

    elif message.text == '💰 Прайс-лист':
        price_list(message)

    elif message.text == '⚙ Настройки':
        settings(message)

    elif message.text == 'ℹ Информация':
        info(message)

    elif message.text == '👔 О нас':
        about(message)

def price_list(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🐒 Лёгкие табаки', '🦍 Крепкие табаки')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, '👤 Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)

def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🏠 Домашний адрес', '📚 История заказов')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, '👤 Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)

def account_info(message):
    if message.text == '🏠 Домашний адрес':
        pass

    elif message.text == '📚 История заказов':
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


if __name__ == '__main__':
    bot.polling(none_stop=True)
