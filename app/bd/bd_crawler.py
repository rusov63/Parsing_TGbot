from pandas import DataFrame
from config import db_manager
from aiogram.types import Message
from app.prices_parser import get_price_from_url

async def create_table():
    """
    Создает таблицу 'products' в базе данных, если она еще не существует.

    Таблица содержит следующие поля:
    - id: уникальный идентификатор продукта (SERIAL PRIMARY KEY)
    - title: название продукта (VARCHAR(255))
    - url: URL продукта (TEXT)
    - xpath: XPath для извлечения цены (TEXT)
    - price: цена продукта (DECIMAL(10,2))
    """
    await db_manager.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            url TEXT,
            xpath TEXT,
            price DECIMAL(10,2)
        )
    """)

async def save_data_to_db(df: DataFrame, message: Message):
    """
    Сохраняет данные о продуктах из DataFrame в базу данных.

    :param:
    - df: DataFrame, содержащий данные о продуктах, включая 'title', 'url' и 'xpath'.
    - message: объект Message из aiogram, используемый для отправки сообщений об ошибках.

    Функция создает таблицу 'products', если она не существует, и заполняет ее данными из DataFrame.
    Если цена не может быть получена, отправляется сообщение об ошибке.
    """
    await create_table()  # Создаем таблицу

    # Заполняем базу данными из DataFrame.
    for _, row in df.iterrows():
        value = await get_price_from_url(row['xpath'])

        if value is not None:
            # Если цена получена успешно, добавляем ее в базу.
            await db_manager.execute(
                "INSERT INTO products (title, url, xpath, price) VALUES ($1, $2, $3, $4)",
                row['title'], row['url'], row['xpath'], value
            )
        else:
            # Если цена не получена, выводим сообщение об ошибке.
            await message.answer(f"Не удалось получить цену для товара '{row['title']}'")