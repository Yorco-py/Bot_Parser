import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot('1313037654:AAH5XwR81Dik5aZzzxR8ZRB74wVr_NVO718')
URL = 'https://goverla.ua/'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('USD')
    itembtn2 = types.KeyboardButton('EUR')
    itembtn3 = types.KeyboardButton('PLN')
    itembtn4 = types.KeyboardButton('GBP')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    msg = bot.send_message(message.chat.id,
                           'Вітаю! Оберіть валюту, яка вас цікавить', reply_markup=markup)
    bot.register_next_step_handler(msg, process_coin_step)

def get_text(URL):
    r = requests.get(URL)
    return r

def process_coin_step(message):
    try:
        markup = types.ReplyKeyboardRemove(selective=False)

        soup = BeautifulSoup(html, 'html.parser')
        coins = soup.find_all('div', class_='gvrl-table')
        buy = soup.find('div', class_='gvrl-table-cell bid')
        sale = soup.find('div', class_='gvrl-table-cell ask')

        for coin in coins:
            if (message.text == coin['gvrl-table']):
                bot.send_message(message.chat.id, printCoin(coin[buy], coin[sale]),
                                 reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Щось пішло не так!')

def printCoin(buy, sale):
    return " *Купівля:* " + str(buy) + "\n *Продаж:* " + str(sale)

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
