from aiogram import F, Router
from aiogram.types import CallbackQuery


user_router = Router()


@user_router.callback_query(F.data == 'Обратная связь')
async def feedback(callback: CallbackQuery) -> CallbackQuery:
    """
    Функция, которая обрабатывает нажатие на кнопку "Обратная связь" в пользовательском интерфейсе.

    :arg: callback (CallbackQuery): Объект, содержащий информацию о нажатии на кнопку.
    :return: Ничего не возвращает, но отправляет сообщение пользователю с инструкциями по обратной связи.
    """
    await callback.message.answer(f'Если вы хотите внести предложения или подчеркнуть проблему сервиса, '
                                  f'напишите руководителю проекта Руслану Овчаренко @rusov63')

    await callback.answer(f'')
