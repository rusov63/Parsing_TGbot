import re
import aiohttp
from bs4 import BeautifulSoup


def process_price(html: str) -> float:
    """
    Извлекает цену из HTML-кода страницы.

    Эта функция принимает HTML-код страницы в виде строки, парсит его с помощью BeautifulSoup
    и ищет цену, используя заранее определенные селекторы. Если цена найдена, она возвращается
    в виде числа с плавающей точкой. Если цена не найдена или возникает ошибка, возвращается None.

    :param html: HTML-код страницы в виде строки.
    :return: Цена товара в виде числа с плавающей точкой или None, если цена не найдена.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        # Список селекторов для поиска цены
        price_selectors = [
            'span[class*="price"]',  # to-toshka.ru, sela
            'bdi',
            'span[style="white-space: nowrap;"]',  # oldos
            'span[id*="price"]',
            '.product-page__price-new',
            'div.price',
            'span.price'
        ]

        for selector in price_selectors:
            price_element = soup.select_one(selector)

            if price_element:
                price_text = price_element.text.strip()
                # Извлекаем только числа с точкой через регулярное выражение
                price = re.findall(r'\d+\.?\d*', price_text)

                if price:
                    return (float(''.join(price)))

                elif price is None:
                    print("Цена не найдена")
                    return None

        print("Цена не найдена")
        return None

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None


async def get_price_from_url(xpath: str) -> float:
    """
    Получает HTML-код страницы по указанному URL и извлекает цену.

    Эта асинхронная функция принимает URL в виде строки, выполняет HTTP-запрос для получения
    HTML-кода страницы и передает его в функцию process_price для извлечения цены. Если
    запрос успешен, возвращается цена. В случае ошибки или если доступ запрещен, возвращается None.

    :param xpath: URL страницы, с которой необходимо получить цену.
    :return: Цена товара в виде числа с плавающей точкой или None в случае ошибки.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(xpath) as response:
                if response.status == 200:
                    html = await response.text()
                    return process_price(html)
                elif response.status == 403:
                    print(f"Доступ запрещен (403) для URL: {xpath}. Пропускаем.")
                    return None
                else:
                    print(f"Ошибка при получении страницы: {response.status}")
                    return None

    except Exception as e:
        print(f"Error: {e}")
        return None