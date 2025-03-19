import asyncio

from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_router = Router()

from typing import NoReturn


@user_router.message(CommandStart())
async def command_start(message: types.Message) -> NoReturn:
    """
    Обрабатывает команду /start от пользователя.

    Отправляет приветственное сообщение и показывает основную клавиатуру с командами.

    :arg:
        message (types.Message): Объект сообщения от пользователя

    :return:
        NoReturn: Функция не возвращает значение
    """
    await message.bot.send_chat_action(chat_id=message.from_user.id,
                                       action=ChatAction.TYPING)
    await asyncio.sleep(.5)

    await message.reply(f'Добро пожаловать пользователь, {hbold(message.from_user.full_name)}!')

    await message.answer(f'Для начала выберите команду: ', reply_markup=keyboard_main())


@user_router.callback_query(F.data == '/start')
async def command(callback: CallbackQuery) -> NoReturn:
    """
    Обрабатывает нажатие inline-кнопки с командой /start.

    Отправляет сообщение с основной клавиатурой и подтверждает callback.

    :arg:
        callback (CallbackQuery): Объект callback-запроса

    :return:
        NoReturn: Функция не возвращает значение
    """
    await callback.bot.send_chat_action(chat_id=callback.message.from_user.id,
                                        action=ChatAction.TYPING)
    await asyncio.sleep(.5)

    await callback.message.answer(f'Для начала выберите команду: ', reply_markup=keyboard_main())

    await callback.answer(f'Стартовая')


def keyboard_main() -> InlineKeyboardMarkup:
    """
    Создает основную inline-клавиатуру бота.

    Клавиатура содержит 2 кнопки:
    - Сборщик информации (/crawler)
    - Обратная связь

    :return:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками
    """
    inline_main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📊 Сборщик информации', callback_data='/crawler')],
        [InlineKeyboardButton(text='📩 Обратная связь', callback_data='Обратная связь')]
    ])

    return inline_main
