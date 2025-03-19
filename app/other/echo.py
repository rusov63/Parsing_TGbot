from aiogram import types, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

echo_router = Router()

@echo_router.message()
async def echo(message: types.Message) -> types.Message | InlineKeyboardMarkup:
    """
    Функция отвечает на сообщение от пользователя если сообщение не распознана как команда.
    """
    await message.answer('Неизвестная команда! \n'
                         'Воспользуйтесь меню или нажмите на кнопку', reply_markup=inline_skf())



def inline_skf():
    """
    Создает и возвращает клавиатуру с одной кнопкой:
    1. "На стартовую" - с callback_data '/start'

    Эта клавиатура может быть использована для навигации пользователя
    в боте, позволяя ему вернуться на главную страницу.

    :return: InlineKeyboardMarkup: Объект клавиатуры с одной кнопкой.
    """
    inline_main = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🚀 На стартовую', callback_data='/start')]
    ])

    return inline_main