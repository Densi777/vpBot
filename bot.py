# -*- coding: utf-8 -*-
import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Главное меню'))
    bot.send_message(message.chat.id, 'Привет!\nДавай начнём!', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def temp():
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
