# -*- coding: utf-8 -*-
from telebot import types
import bot_main
from bot_main import bot


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
    msg = bot.send_message(message.chat.id, 'Напишите адрес доставки\nИли отправьте местоположение', reply_markup=keyboard)
    bot.register_next_step_handler(msg, address_or_location)


def address_or_location(message):
    if message.text != '📍 Местоположение':
        print(message.text)
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
        bot_main.main_menu(message)
