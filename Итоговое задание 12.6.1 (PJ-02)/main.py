# Автор: Haron
# Дата: 13.03.24

import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение
    bot.send_message(message.chat.id, f"Приветствую, {message.chat.username}")
    # Вызов функции help для отправки инструкций
    help(message)


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    # Инструкции для пользователя
    instructions = 'Чтобы начать работу, введите команду в следующем формате: \
    \n\n<Имя валюты, цену которой вы хотите узнать> \
    \n<Имя валюты, в которой надо узнать цену первой валюты> \
    \n<Количество первой валюты> \
    \n\nНапример: доллар рубль 5 \
    \n\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, instructions)


# Обработчик команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # Отправка списка доступных валют
    available_currencies = 'Доступные валюты:'
    for key in keys.keys():
        available_currencies = '\n'.join((available_currencies, key))
    bot.send_message(message.chat.id, available_currencies)

@bot.message_handler(commands=['avtor'])
def show_author(message):
    bot.send_message(message.chat.id, "Этот код написал Haron, 13 марта 2024 года.")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        # Проверка корректности ввода
        if len(values) != 3:
            raise ConvertionException('Неверный формат ввода')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду:\n{e}')
    else:
        # Отправка результата конвертации
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
