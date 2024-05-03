import telebot
import yfinance as yf
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('7013394931:AAHkuDtpgl4XCkGuSKw5g6elFw3EuFBQ3zs')

# Расширенный список названий акций и валют
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA',
          'NFLX', 'FB', 'NVDA', 'INTC', 'AMD',
          'PYPL', 'IBM', 'V', 'MA', 'CSCO',
          'DIS', 'UBER', 'SBUX', 'KO', 'WMT']

currencies = {'USD': {'name': 'USD', 'description': 'Доллар США'},
              'EUR': {'name': 'EUR', 'description': 'Евро'},
              'GBP': {'name': 'GBP', 'description': 'Фунт стерлингов'},
              'RUB': {'name': 'RUB', 'description': 'Российский Рубль'}}

user_data = {}


# Функция для получения цены акции в выбранной валюте и ссылки на Yahoo Finance
def get_stock_info(stock_name, currency):
    stock = yf.Ticker(stock_name)
    stock_data = stock.history(period='1d')

    if not stock_data.empty:
        last_price = stock_data['Close'].iloc[-1]

        if currency == 'RUB':
            converted_price = last_price * 74.0  # Пример конвертации в рубли (можно заменить на актуальный курс)
        else:
            converted_price = last_price

        yahoo_finance_link = f"https://finance.yahoo.com/quote/{stock_name}"
        return f"Цена акций {stock_name} сегодня: {converted_price:.2f} {currency}\n\n" \
               f"Ссылка на подробную информацию: {yahoo_finance_link}"
    else:
        return None


# Обработчики сообщений
@bot.message_handler(commands=['start'])
def start(message):
    markup_stocks = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for stock in stocks:
        markup_stocks.add(stock)

    bot.send_message(message.chat.id, "Выберите акцию из списка:", reply_markup=markup_stocks)


@bot.message_handler(func=lambda message: message.text in stocks)
def select_stock(message):
    user_id = message.chat.id
    user_data[user_id] = {'stock': message.text.upper(), 'step': 'currency'}

    markup_currencies = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cur_data in currencies.values():
        markup_currencies.add(cur_data['name'])

    bot.send_message(user_id, "Выберите валюту для конвертации:", reply_markup=markup_currencies)


@bot.message_handler(func=lambda message: message.text in currencies.keys())
def convert_currency(message):
    user_id = message.chat.id
    if user_id in user_data and user_data[user_id]['step'] == 'currency':
        currency = message.text.upper()
        user_data[user_id]['currency'] = currency
        stock_name = user_data[user_id]['stock']

        stock_info = get_stock_info(stock_name, currency)
        if stock_info is not None:
            bot.send_message(user_id, stock_info)

            user_data[user_id]['step'] = 'stock'  # После получения цены, переходим на следующий шаг выбора акции
            markup_stocks = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for stock in stocks:
                markup_stocks.add(stock)
            bot.send_message(user_id, "Выберите следующую акцию:", reply_markup=markup_stocks)
        else:
            bot.send_message(user_id, "Данные об акции не найдены. Пожалуйста, попробуйте другую акцию.")
    else:
        bot.reply_to(message, "Выберите валюту из списка.")


# Запуск бота
bot.polling()