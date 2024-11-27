
from aiogram import Router, F, types
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup
from bot_config import groups, database


group_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=group, callback_data=group)] for group in groups
    ]
)

homework_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 9)]
    ]
)


class HomeworkStates(StatesGroup):
    name = State()
    group = State()
    homework_number = State()
    github_link = State()

hw_router = Router()

@hw_router.callback_query(F.data == "send_hw")
async def send_hw_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, введите ваше имя:")
    await state.set_state(HomeworkStates.name)
    await callback.answer()

@hw_router.message(HomeworkStates.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer("Введите ваше имя без различный символов и цифр.")
        return
    name = name.capitalize()
    await state.update_data(name=name)
    await state.set_state(HomeworkStates.group)
    await message.answer("Выберите вашу группу:", reply_markup=group_keyboard)

@hw_router.callback_query(HomeworkStates.group)
async def process_group(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(group=callback.data)
    await state.set_state(HomeworkStates.homework_number)
    await callback.message.answer("Выберите номер домашнего задания:", reply_markup=homework_keyboard)
    await callback.answer()

@hw_router.callback_query(HomeworkStates.homework_number)
async def process_homework(callback: types.CallbackQuery, state: FSMContext):
    if 1 <= int(callback.data) <= 8:
        await state.update_data(homework_number=int(callback.data))
        await state.set_state(HomeworkStates.github_link)
        await callback.message.answer("Отправьте ссылку на GitHub репозиторий:")
    else:
        await callback.answer("Неверный номер домашнего задания")
    await callback.answer()

@hw_router.message(HomeworkStates.github_link)
async def process_github(message: types.Message, state: FSMContext):
    if message.text.startswith('https://github.com'):
        await state.update_data(github_link=message.text)
        data = await state.get_data()

        database.save_homework(
            name=data['name'],
            group_name=data['group'],
            homework_number=data['homework_number'],
            github_link=data['github_link']
        )
        await message.answer("Домашнее задание сохранено!")
        await state.clear()
    else:
        await message.answer("Ссылка должна начинаться с 'https://github.com'")
