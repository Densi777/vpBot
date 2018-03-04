# -*- coding: utf-8 -*-
import telebot
import config
from telebot import types
import datetime

bot = telebot.TeleBot(config.token)
greetings = ('Здравствуй', 'Привет', 'Доброго времени суток')


@bot.message_handler(commands=['start'])
def start(message):
    now = datetime.datetime.now()
    today = now.day
    hour = now.hour

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(choice) for choice in ['Главное меню', 'Error']])
    msg = bot.send_message(message.chat.id, 'Привет!\nДавай начнём!', reply_markup=keyboard)
    bot.register_next_step_handler(msg, choice)

def choice(message):
    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, '1')
    elif message.text == 'Error':
        bot.send_message(message.chat.id, '2')


if __name__ == '__main__':
    bot.polling(none_stop=True)
