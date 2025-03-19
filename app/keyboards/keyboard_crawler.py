from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def cancel_keyboard():

    cancel_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return cancel_keyboard