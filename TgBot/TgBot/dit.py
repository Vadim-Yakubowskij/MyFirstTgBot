import webbrowser

import telebot

bot = telebot.TeleBot('7013394931:AAHkuDtpgl4XCkGuSKw5g6elFw3EuFBQ3zs')


@bot.message_handler(commands=['open_site', 'site'])
def site(message):
    webbrowser.open('https://vadim-yakubowskij.github.io/Podarok/')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,
                     f'Вы успешно запустили меня, {message.from_user.first_name} {message.from_user.last_name}!')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'Ваш ID: {message.from_user.id}')


bot.polling(none_stop=True)
