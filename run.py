import asyncio
import logging
import sys

from aiogram.utils.token import TokenValidationError

import bot_start
from app import handler_main
from app.other import feedback_project, echo

from config import dp, bot, ADMIN_ID, db_manager

from aiogram.types import BotCommand, BotCommandScopeDefault


async def on_startup():
    #await db_manager.connect() # connect to bd
    await bot.send_message(chat_id=ADMIN_ID, text=f'🤩 Бот запущен!')


async def on_shutdown():
    await bot.send_message(chat_id=ADMIN_ID, text=f'🤨 Внимание, бот остановлен!')
    # Закрываем сессию бота, освобождая ресурсы
    await bot.session.close()


async def set_commands():
    """Командное меню. Дефолтное значение"""

    commands = [
        BotCommand(command='/start', description='Старт'),
        BotCommand(command='/crawler', description='Сборщик информации')
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    try:
        dp.include_routers(
            bot_start.user_router,
            feedback_project.user_router,
            handler_main.crawler_router,
            echo.echo_router
        )

        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        await db_manager.connect()
        await set_commands()
        await dp.start_polling(bot)

    except TokenValidationError:
        logging.error('Бота не удалось авторизовать. Проверьте токен.')
        raise
    except Exception as e:
        logging.error(f'Произошла ошибка: {e}')
        raise


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    if True:
        try:
            asyncio.run(main())
        except TokenValidationError:
            logging.error('Бота не удалось авторизовать. Проверьте токен.')
            sys.exit(1)
        except Exception as e:
            logging.error(f'Произошла неожиданная ошибка: {e}')
            sys.exit(1)
    elif False:
        print("exit")
