# -*- coding: utf-8 -*-
import telebot
import config
import inf
from telebot import types
import datetime

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def mainMenu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📝Заказать', 'Корпоратив')
    keyboard.row('💰Прайс-лист', '🔧Настройки')
    keyboard.row(⚠'Информация', '👔О нас')
    msg = bot.send_message(message.chat.id, '📖Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)

def menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == '🔧Настройки':
        settings(message)

    elif message.text == '⚠Информация':
        info(message)

    elif message.text == '👔О нас':
        about(message)

def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🏠Домашний адрес', '📚История заказов')
    keyboard.row('↪Назад')
    msg = bot.send_message(message.chat.id, '👤Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)

def account_info(message):
    if message.text == '🏠Домашний адрес':
        pass

    elif message.text == '📚История заказов':
        pass

    elif message.text == '↪Назад':
        mainMenu(message)


def about(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪Назад')
    msg = bot.send_message(message.chat.id, inf.about_us, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)

def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪Назад')
    msg = bot.send_message(message.chat.id, inf.info_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
