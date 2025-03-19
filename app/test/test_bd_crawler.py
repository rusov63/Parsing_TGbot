import unittest
from unittest.mock import AsyncMock, patch, call
from pandas import DataFrame
from aiogram.types import Message

from app.bd.bd_crawler import save_data_to_db


class TestSaveDataToDb(unittest.IsolatedAsyncioTestCase):

    @patch('app.bd.bd_crawler.db_manager')
    @patch('app.prices_parser.get_price_from_url')
    async def test_save_data_to_db(self, mock_get_price_from_url, mock_db_manager):
        # Mock the database manager and price parser
        mock_db_manager.execute = AsyncMock()
        mock_get_price_from_url.return_value = 100.0

        mock_message = AsyncMock(spec=Message)
        mock_message.answer = AsyncMock()

        # Create a test DataFrame
        df = DataFrame({
            'title': ['Product 1'],
            'url': ['http://example.com/product1'],
            'xpath': ['http://example.com/product2']
        })

        await save_data_to_db(df, mock_message)

        create_table_call = call(
            "CREATE TABLE IF NOT EXISTS products ("
            "id SERIAL PRIMARY KEY,"
            "title VARCHAR(255),"
            "url TEXT,"
            "xpath TEXT,"
            "price DECIMAL(10,2)"
            ")"
        )
        mock_db_manager.execute.assert_any_call(create_table_call.args[0])

        mock_get_price_from_url.assert_called_once_with('http://example.com/product2]')
        mock_db_manager.execute.assert_any_call(
            "INSERT INTO products (title, url, xpath, price) VALUES ($1, $2, $3, $4)",
            'Product 1', 'http://example.com/product1', 'http://example.com/product2]', 100.0
        )


        mock_message.answer.assert_not_called()

    @patch('app.bd.bd_crawler.db_manager')
    @patch('app.prices_parser.get_price_from_url')
    async def test_save_data_to_db_price_not_found(self, mock_get_price_from_url, mock_db_manager):

        mock_db_manager.execute = AsyncMock()
        mock_get_price_from_url.return_value = None

        mock_message = AsyncMock(spec=Message)
        mock_message.answer = AsyncMock()

        df = DataFrame({
            'title': ['Product 1'],
            'url': ['http://example.com/product1'],
            'xpath': ['http://example.com/product2']
        })

        await save_data_to_db(df, mock_message)

        create_table_call = call(
            "CREATE TABLE IF NOT EXISTS products ("
            "id SERIAL PRIMARY KEY,"
            "title VARCHAR(255),"
            "url TEXT,"
            "xpath TEXT,"
            "price DECIMAL(10,2)"
            ")"
        )
        mock_db_manager.execute.assert_any_call(create_table_call.args[0])

        mock_get_price_from_url.assert_called_once_with('//span[@class="price"]')

        mock_message.answer.assert_called_once_with("Не удалось получить цену для товара 'Product 1'")


if __name__ == '__main__':
    unittest.main()
