# -*- coding: utf-8 -*-
import telebot
import config
import inf
from telebot import types

bot = telebot.TeleBot(config.token)


@bot.message_handler(func=lambda message: True, commands=['start'])
def main_menu(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('📝 Заказать', '🥂 Корпоратив')
    keyboard.row('💰 Прайс-лист', '⚙ Настройки')
    keyboard.row('ℹ Информация', '👔 О нас')
    msg = bot.send_message(message.chat.id, '📖 Главное меню:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu)


def menu(message):
    if message.text == '📝 Заказать':
        order_tobacco(message)

    elif message.text == '🥂 Банкет':
        config.excount += 100
        banquet(message)

    elif message.text == '💰 Прайс-лист':
        price_list(message)

    elif message.text == '⚙ Настройки':
        settings(message)

    elif message.text == 'ℹ Информация':
        info(message)

    elif message.text == '👔 О нас':
        about(message)


def order_tobacco(message):
    print(message.chat.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🐒 Лёгкий', '🦍 Крепкий')
    msg = bot.send_message(message.chat.id, 'Выберите крепкость кальяна:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, order_tobacco_get)


def order_tobacco_get(message):
    if message.text == '🐒 Лёгкий':
        order_cups(message)

    elif message.text == '🦍 Крепкий':
        config.excount += 10
        order_cups(message)


def order_cups(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Отправить')
    msg = bot.send_message(message.chat.id, 'Напишите адрес доставки', reply_markup=keyboard)
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


def close_order(message):
    if message.text == '✔ Завершить':
        if config.excount == 1:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\n1 чаша\nПо адресу:\n' + config.address)

        elif config.excount == 2:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\n2 чаши\nПо адресу:\n' + config.address)

        elif config.excount == 3:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\n3 чаши\nПо адресу:\n' + config.address)

        elif config.excount == 4:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nЛёгкий кальян\nБолее трёх чаш\nПо адресу:\n' + config.address)

        elif config.excount == 11:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n1 чаша\nПо адресу:\n' + config.address)

        elif config.excount == 12:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n2 чаши\nПо адресу:\n' + config.address)

        elif config.excount == 13:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\n3 чаши\nПо адресу:\n' + config.address)

        elif config.excount == 14:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\nБолее трёх чаш\nПо адресу:\n' + config.address)

        elif config.excount == 120:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nБанкет\nДо 5 человек\nПо адресу:\n' + config.address)

        elif config.excount == 121:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\nБолее 5 человек\nПо адресу:\n' + config.address)

        elif config.excount == 122:
            bot.send_message(chat_id=config.my_id, text='Заказ:\nКрепкий кальян\nБолее 10 человек\nПо адресу:\n' + config.address)
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
    bot.register_next_step_handler(msg, tobacco_prices)


def tobacco_prices_get(message):
    if message.text == 'Лёгкий':
        bot.send_message(message.chat.id, inf.easy_tobacco)
        price_list(message)

    elif message.text == 'Крепкий':
        bot.send_message(message.chat.id, inf.hard_tobacco)
        price_list(message)

    elif message.text == '↪ Назад':
        main_menu(message)


def settings(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🏠 Домашний адрес', '📚 История заказов')
    keyboard.row('↪ Назад')
    msg = bot.send_message(message.chat.id, '👤 Аккаунт:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, account_info)


def account_info(message):
    if message.text == '🏠 Домашний адрес':
        set_home_address(message)

    elif message.text == '📚 История заказов':
        bot.send_message(message.chat.id, 'Empty')
        settings(message)

    elif message.text == '↪ Назад':
        main_menu(message)


def set_home_address(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Сохранить')
    msg = bot.send_message(message.chat.id, 'Введите домашний адрес:', reply_markup=keyboard)
    bot.register_next_step_handler(msg, save_address)


def save_address(message):
    if message.text == 'Сохранить':
        bot.send_message(message.chat.id, 'Сохранено')
        account_info(message)


def about(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('↪ Назад')
    msg = bot.send_message(message.chat.id, inf.about_us, reply_markup=keyboard)
    bot.register_next_step_handler(msg, main_menu)


def info(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Правила предоставления услуг')
    keyboard.row('Штрафы')
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

    elif message.text == '↪ Назад':
        main_menu(message)


bot.polling(none_stop=True)
