from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from parser import parser, search_parser
import asyncio

bot = Bot(token='6989175958:AAFah4VCpvTE_1lj6rsCxAeUd51nmps5ZLo')
dp = Dispatcher(bot=bot)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Для выдачи порно введи слово "/random"\nДля поиска вводи /search [запрос]')


@dp.message(Command("random"))
async def cmd_test1(message: types.Message):
    await message.reply(parser())


@dp.message(Command("search"))
async def cmd_test1(message: types.Message):
    user_request = message.text.split(' ')[1:]
    await message.reply(search_parser('+'.join(user_request)))


async def main():
    await dp.start_polling(bot, skip_updates=True)


# Test commit

if __name__ == '__main__':
    asyncio.run(main())
