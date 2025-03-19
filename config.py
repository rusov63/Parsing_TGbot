from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from asyncpg import create_pool, Pool

load_dotenv()

# инициируем объект бота
dp: Dispatcher = Dispatcher()

# Админ
ADMIN_ID: int = int(os. getenv('ADMIN_ID'))

# Загружаем переменные из.env
TOKEN: str = str(os.getenv('BOT_TOKEN'))


# Взамодействие с базой данных.
class DatabaseManager:
    def __init__(self):
        self.pool: Pool = None

    async def connect(self):
        self.pool = await create_pool(os.getenv('PG_LINK'), min_size=1, max_size=10)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

db_manager = DatabaseManager()


# инициируем объект бота, передавая ему parse_mode=ParseMode.HTML по умолчанию
bot: Bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


SLEEP_TIME: int = 2

CHUNK_SIZE: int = 3500


# хранения данных FSM Redis
#redis_url = os.getenv('REDIS_URL')

# используется для хранения данных конечного автомата состояний (FSM) в Redis.
#storage = RedisStorage.from_url(os.getenv('REDIS_URL'))
