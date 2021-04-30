from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from Parser import parseURL
from states.States import Form, Test

from loader import bot
from loader import dp
from utils.db_api.dp_api import db


@dp.message_handler(CommandStart(), state=None)
async def send_welcome(message: types.Message, state: FSMContext):
    await db.add_new_user()
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['Новости'], state=None)
async def get_url(message: types.Message, state: FSMContext):
    await Form.parse.set()
    await bot.send_message(message.chat.id, 'Введите ссылку на канал')

    # комментарий для коммита

@dp.message_handler(commands=['Сбросить'], state="*")
async def removeState(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, 'Текущее состояние было обнулено')


@dp.message_handler(state=Form.parse, content_types=types.ContentTypes.TEXT)
async def parse(message: types.Message, state: FSMContext):
    url = message.text
    await parseURL(url)
    await state.finish()


@dp.message_handler(commands=['Канал'], state=None)
async def addChanel(message: types.Message, state: FSMContext):
    await Test.t1.set()
    await bot.send_message(message.chat.id, "Введите назавание канала")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t1)
async def setChannel(message: types.Message, state: FSMContext):
    channel = message.text
    await db.add_channel_to_news_feed(channel)
    await bot.send_message(message.chat.id, "канал добавлен!")
    await state.finish()




