from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command('start'))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отправить д/з", callback_data="send_hw"
                )
            ]
        ]
    )
    await message.answer(
        f"Здравствуйте, {name}!\n"
        f"Наш бот помогает с отправкой д/з Игорю!",
        reply_markup=kb
    )