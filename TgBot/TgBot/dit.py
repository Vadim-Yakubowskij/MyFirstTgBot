import webbrowser
from telebot import types
import telebot

bot = telebot.TeleBot('7013394931:AAHkuDtpgl4XCkGuSKw5g6elFw3EuFBQ3zs')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт')
    btn2 = types.InlineKeyboardButton('Удалить фото')
    btn3 = types.InlineKeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    markup.row(btn1)
    bot.send_message(message.chat.id,
                     f'Вы успешно запустили меня, {message.from_user.first_name} {message.from_user.last_name}!', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://vadim-yakubowskij.github.io/Podarok/')
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    markup.row(btn1)
    bot.reply_to(message, 'Классное фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['open_site', 'site'])
def site(message):
    webbrowser.open('https://vadim-yakubowskij.github.io/Podarok/')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Ваш ID: {message.from_user.id}')
    elif message.text.lower() == 'красавчик баля':
        bot.send_message(message.chat.id,
                         f'Спасибо ты тоже ебать тип, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'внатуре красавчик':
        bot.reply_to(message, 'от души брат')


bot.polling(none_stop=True)
