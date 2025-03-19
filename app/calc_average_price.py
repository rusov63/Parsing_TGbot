from aiogram import types
import pandas as pd
from config import db_manager


async def calculate_average_price():
    """
    Рассчитывает средние цены товаров из базы данных.

    Функция извлекает данные о товарах из таблицы `products`,
    проверяет наличие цен и рассчитывает средние цены для каждого товара
    по его URL. Возвращает DataFrame с результатами.

    :raise:
        ValueError: Если в базе данных нет данных или произошла ошибка при расчете.
    """
    try:
        # Получаем данные из базы
        rows = await db_manager.execute("SELECT title, url, price FROM products")

        # Проверяем, есть ли данные
        if not rows:
            raise ValueError("В базе данных нет данных")

        # Преобразуем результат в список кортежей
        data = [(row['title'], row['url'], float(row['price']))
                for row in rows if row['price'] is not None]

        # Создаем DataFrame
        df = pd.DataFrame(data, columns=['title', 'url', 'price'])

        # Группируем и считаем среднее
        #average_prices = df.groupby(['url', 'title'])['price'].mean().reset_index()
        average_prices = df.groupby(['url', 'title']).agg({'price': 'mean'}).reset_index()

        return average_prices

    except Exception as e:
        print(f"Ошибка в функции calculate_average_price: {str(e)}")
        raise ValueError("Error calculating average prices")


async def show_average_price(message: types.Message):
    """
     Отправляет пользователю сообщение со средними ценами товаров.

     Функция вызывает calculate_average_price для получения средних цен
     и формирует строку с результатами, которую отправляет пользователю
     через Telegram.

     :arg:
         message (types.Message): Сообщение от пользователя,
         в которое будет отправлен ответ.

     :raise:
         Exception: Если произошла ошибка при расчете средней цены.
     """
    try:
        # Рассчитываем средние цены
        average_prices = await calculate_average_price()

        # Формируем строку для вывода
        result = "Средние цены товаров по сайтам:\n"
        for _, row in average_prices.iterrows():
            result += f"Товар: {row['title']}, Сайт: {row['url']}, Средняя цена: {row['price']:.2f}\n"

        await message.answer(result)

    except Exception as e:
        await message.answer(f"Произошла ошибка при расчете средней цены: {str(e)}")