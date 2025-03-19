from typing import Optional
import asyncio
import pandas as pd
from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.filters import Command
import os
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from app.bd.bd_crawler import save_data_to_db
from app.calc_average_price import show_average_price
from app.correct_data import check_excel_data, check_correct_columns
from app.keyboards.keyboard_crawler import cancel_keyboard
from config import SLEEP_TIME, CHUNK_SIZE, bot

crawler_router = Router()


@crawler_router.message(Command('crawler'))
async def start_crawler(message: types.Message) -> None:
    """
    Обработчик команды /crawler для начала работы с краулером

    :arg: message: Объект сообщения от пользователя

    :return: None
    """
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action=ChatAction.TYPING)
    await asyncio.sleep(SLEEP_TIME)

    await message.answer("Пожалуйста, прикрепите Excel файл с колонками 'title', 'url' и 'xpath'\n"
                         "Для этого нажмите на значок скрепки 📎 и выберите файл",
                         reply_markup=cancel_keyboard()
                         )


@crawler_router.callback_query(F.data == '/crawler')
async def start_callbacks(callback: CallbackQuery) -> None:
    """
    Обработчик callback-запроса для команды /crawler

    :arg: callback: Объект callback-запроса

    :return: None
    """
    await callback.bot.send_chat_action(chat_id=callback.message.from_user.id,
                                        action=ChatAction.TYPING)
    await asyncio.sleep(.1)

    await callback.answer()
    await callback.message.answer(f'Выбрали: Сборщик информации')
    await callback.message.answer("Пожалуйста, прикрепите Excel файл с колонками 'title', 'url' и 'xpath'\n"
                                  "Для этого нажмите на значок скрепки 📎 и выберите файл",
                                  reply_markup=cancel_keyboard()
                                  )


@crawler_router.message(F.text == "❌ Отмена")
async def cancel_operation(message: types.Message) -> None:
    """
    Обработчик отмены операции

    :arg: message: Объект сообщения от пользователя

    :return: None
    """
    await message.answer("Операция отменена", reply_markup=ReplyKeyboardRemove())


@crawler_router.message(F.document)
async def get_document(message: types.Message) -> Optional[str]:
    """
    Обработчик загрузки документа

    :arg: message: Объект сообщения с документом

    :return: Optional[str]: Сообщение об ошибке или None при успешной обработке
    """
    try:
        await message.bot.send_chat_action(chat_id=message.from_user.id,
                                           action=ChatAction.UPLOAD_DOCUMENT)
        document = message.document

        res = await check_excel_data(document)
        if res is None:
            await message.reply("Пожалуйста, загрузите файл в формате Excel (.xlsx)")
            return

        await message.answer("Обработка файла...")

        file = await bot.get_file(document.file_id)
        file_path = f"downloads/{document.file_name}"

        os.makedirs("downloads", exist_ok=True)

        await bot.download_file(file.file_path, file_path)

        df = pd.read_excel(file_path)

        res = await check_correct_columns(df)
        if res is None:
            await message.reply("В файле отсутствуют необходимые колонки (title, url, xpath)")
            return

        df_string = df.to_string()
        chunks = [df_string[i:i + CHUNK_SIZE] for i in range(0, len(df_string), CHUNK_SIZE)]

        await message.answer("Содержимое файла:")
        for chunk in chunks:
            await asyncio.sleep(SLEEP_TIME)
            await message.answer(chunk)

        await message.answer('Сохраняем в БД...')
        await asyncio.sleep(SLEEP_TIME)
        size = ["Файл большой, еще чуть чуть..." if len(df_string) >= CHUNK_SIZE else "Почти все готово!"]
        await message.answer(*size)

        await save_data_to_db(df, message)
        await message.answer('Данные сохранены в БД')
        await message.answer(f'Файл {document.file_name} успешно обработан!')

        os.remove(file_path)

        await show_average_price(message)

    except asyncio.TimeoutError:
        await message.answer("Превышено время ожидания при загрузке файла")

    except FileNotFoundError:
        await message.answer("Файл не найден")

    except Exception as e:
        await message.answer(f"Произошла ошибка при обработке файла: {str(e)}")
