# Автор: Haron
# Дата: 13.03.24

import requests
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        """
        Получает цену валюты на основе переданных параметров.

        Args:
            quote (str): Имя валюты, цену которой нужно узнать.
            base (str): Имя валюты, в которой нужно узнать цену первой валюты.
            amount (str): Количество первой валюты.

        Returns:
            float: Цена указанного количества валюты в заданной валюте.
        """
        if quote == base:
            raise ConvertionException(f'Вы не можете перевести {quote} в {base}')

        # Получаем коды валют из словаря keys
        quote_ticker = keys.get(quote)
        base_ticker = keys.get(base)

        # Проверяем наличие кодов валют в словаре keys
        if not quote_ticker:
            raise ConvertionException(f'Валюта {quote} не найдена')
        if not base_ticker:
            raise ConvertionException(f'Валюта {base} не найдена')

        # Пытаемся преобразовать количество валюты в число
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Количество {amount} не является числом')

        # Формируем URL для запроса к API
        url = f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}'
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code != 200:
            raise ConvertionException('Ошибка при получении данных')

        # Получаем данные из ответа и извлекаем цену
        data = response.json()
        total_base = data.get(base_ticker)

        # Проверяем, получена ли цена
        if total_base is None:
            raise ConvertionException('Ошибка при обработке данных')

        # Вычисляем общую цену и округляем до двух знаков после запятой
        return round(total_base * amount, 2)
