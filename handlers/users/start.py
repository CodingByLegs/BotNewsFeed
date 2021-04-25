from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from Parser import parseURL
from states.States import Form

from loader import bot
from loader import dp


@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['Новости'])
async def get_url(message: types.Message):
    await Form.parse.set()
    await bot.send_message(message.chat.id, 'Введите ссылку на канал')


@dp.message_handler(state=Form.parse, content_types=types.ContentTypes.TEXT)
async def parse(message: types.Message, state: FSMContext):
    url = message.text
    await parseURL(url)
    await state.finish()