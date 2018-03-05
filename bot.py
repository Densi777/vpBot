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
    keyboard.add(*[types.KeyboardButton(menu) for menu in ['Заказать', 'Корпоратив', 'Прайс-лист', 'Настройки', 'Информация', 'О нас']])
    msg = bot.send_message(message.chat.id, 'Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)

def menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'Настройки':
        settings(message)

    elif message.text == 'Информация':
        info(message)

    elif message.text == 'О нас':
        about(message)

def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(account_info) for account_info in ['Домашний адрес', 'История заказов', 'Назад']])
    msg = bot.send_message(message.chat.id, 'Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)

def account_info(message):
    if message.text == 'Домашний адрес':
        pass

    elif message.text == 'История заказов':
        pass

    elif message.text == 'Назад':
        mainMenu(message)


def about(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Назад')
    msg = bot.send_message(message.chat.id, inf.about_us, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)

def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Назад')
    msg = bot.send_message(message.chat.id, inf.info_text, reply_markup=keyboard)
    bot.register_next_step_handler(msg, mainMenu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
