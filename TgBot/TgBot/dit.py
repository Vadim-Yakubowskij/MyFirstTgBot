import webbrowser
from telebot import types
import telebot
import requests
import json

bot = telebot.TeleBot('7013394931:AAHkuDtpgl4XCkGuSKw5g6elFw3EuFBQ3zs')
API = '7421bc9427bcd112b1cfd8b2fd1c8a64'


@bot.message_handler(commands=['love'])
def site(message):
    bot.send_message(message.chat.id, 'Я тебя очень сильно люблю не грусти пожалуйста и покушай обязательно❤️ ')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f'Вы успешно запустили меня, {message.from_user.first_name} {message.from_user.last_name}!')
    bot.send_message(message.chat.id,
                     'Напиши название любого города что бы узнать какая там сейчас погода!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if result.status_code == 200:
        data = json.loads(result.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Погода в {city}: {temp} °C')
        ans1 = 'На улице светит яркое солнышко, но не ярче чем ты😍'
        ans2 = 'Облака закрыли солнышко, но с одним таким солнышком я сейчас общаюсь❤️'
        advice = ans1 if temp > 10.0 else ans2
        bot.send_message(message.chat.id, advice)
    else:
        bot.send_message(message.chat.id, 'К сожалению я не знаю такого города😭')


bot.polling(none_stop=True)
