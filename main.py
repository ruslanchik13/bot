
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from parser import parser, search_parser
import asyncio

bot = Bot(token='6989175958:AAFah4VCpvTE_1lj6rsCxAeUd51nmps5ZLo')
dp = Dispatcher(bot=bot)


class OrderFood(StatesGroup):
    count = State()


@dp.message(CommandStart())
async def start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer('Для выдачи порно введи слово "/random"\nДля поиска вводи /search [запрос]',
                         reply_markup=keyboard)


@dp.message(F.text == 'hi')
async def hello(message: types.Message):
    await message.answer('Привет')


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    await message.reply(parser())


@dp.message(Command("search"))
async def cmd_test2(message: types.Message, state: FSMContext):
    await state.update_data(index=0)
    user_request = message.text.split(' ')[1:]
    await state.update_data(videos=search_parser('+'.join(user_request)))
    data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=">",
        callback_data="next")
    )
    await message.answer(
        str(data['videos'][0]),
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "back")
async def back_video(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    builder = InlineKeyboardBuilder()
    if data["index"] != 0:
        await state.update_data(index=data['index'] - 1)
    updated_data = await state.get_data()
    builder.add(types.InlineKeyboardButton(
        text="<",
        callback_data="back"
    )).add(types.InlineKeyboardButton(
        text=">",
        callback_data="next"
    ))
    await callback.message.edit_text(str(updated_data['videos'][updated_data['index']]), reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(F.data == "next")
async def next_video(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    data = await state.get_data()
    await state.update_data(index=data['index'] + 1)
    updated_data = await state.get_data()
    builder.add(types.InlineKeyboardButton(
        text="<",
        callback_data="back"
    )).add(types.InlineKeyboardButton(
        text=">",
        callback_data="next"
    ))
    await callback.message.edit_text(str(updated_data['videos'][updated_data['index']]), reply_markup=builder.as_markup())
    await callback.answer()


async def main():
    await dp.start_polling(bot, skip_updates=True)


# Test commit

if __name__ == '__main__':
    asyncio.run(main())
