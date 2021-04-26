from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from Parser import parseURL
from states.States import Form

from loader import bot
from loader import dp


@dp.message_handler(CommandStart(), state=None)
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['Новости'], state=None)
async def get_url(message: types.Message, state: FSMContext):
    await Form.parse.set()
    await bot.send_message(message.chat.id, 'Введите ссылку на канал')
    data = MyData
    await bot.send_message(message.chat.id, data['key'] + " " + data['key2'])


@dp.message_handler(state=Form.parse, content_types=types.ContentTypes.TEXT)
async def parse(message: types.Message, state: FSMContext):
    url = message.text
    await parseURL(url)
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.loadingh)
async def setUpdate(message: types.Message, state: FSMContext):
    await state.update_data(key=message.text.lower())
    await Form.next()
    await state.update_data(key2=message.text.lower() + "00")
    await bot.send_message(message.chat.id, "Updated")


@dp.message_handler(commands=['n'], state=Form.show)
async def show(message: types.Message, state: FSMContext):
    global MyData
    MyData = await state.get_data()
    await bot.send_message(message.chat.id, MyData['key'] + " " + MyData['key2'])
    await state.finish()


@dp.message_handler(commands=['m'])
async def get_url(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "you wrote /m")
    await Form.loadingh.set()




