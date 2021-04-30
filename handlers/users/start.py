from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

import json
from Parser import parseURL, dump_all_messages
from states.States import Form, Test

from loader import bot
from loader import dp
#from utils.db_api.dp_api import db


@dp.message_handler(CommandStart(), state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    #await db.add_new_user()
    await message.reply("Привет, пользователь")
    await state.finish()


@dp.message_handler(commands=['Новости'], state=None)
async def get_url(message: types.Message):
    await Form.parse.set()
    await bot.send_message(message.chat.id, 'Введите ссылку на канал')


@dp.message_handler(commands=['Сбросить'], state="*")
async def removeState(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, 'Текущее состояние было обнулено')


@dp.message_handler(state=Form.parse, content_types=types.ContentTypes.TEXT)
async def parsing(message: types.Message, state: FSMContext):
    url = message.text
    await dump_all_messages(url)
    await state.update_data(message_id=message.chat.id)
    print(message.chat.id)
    await Form.next()
    tmp = await state.get_data()
    print(tmp['message_id'])
    await loading(state)


@dp.message_handler(commands=['Канал'], state=None)
async def addChanel(message: types.Message, state: FSMContext):
    await Test.t1.set()
    await bot.send_message(message.chat.id, "Введите назавание канала")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t1)
async def setChannel(message: types.Message, state: FSMContext):
    channel = message.text
   #await db.add_channel_to_news_feed(channel)
    await bot.send_message(message.chat.id, "канал добавлен!")
    await state.finish()


@dp.message_handler(commands=['Категория'], state=None)
async def addCategory(message: types.Message, state: FSMContext):
    await Test.t4.set()
    await bot.send_message(message.chat.id, "Введите назавание категории")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t4)
async def setCategory(message: types.Message, state: FSMContext):
    isCustom = True
    category = message.text
    #await db.add_new_category(category, isCustom)
    await bot.send_message(message.chat.id, "Категория добавлена!")
    await state.finish()


@dp.message_handler(commands=['КатегорияУдалить'], state=None)
async def addCategory(message: types.Message, state: FSMContext):
    await Test.t5.set()
    await bot.send_message(message.chat.id, "Введите назавание категории")

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t5)
async def removeCategory(message: types.Message, state: FSMContext):
    category = message.text
    #await db.remove_category(category)
    await bot.send_message(message.chat.id, "Категория удалена!")
    await state.finish()

@dp.message_handler(commands=['КаналУдалить'], state=None)
async def addChanel1(message: types.Message, state: FSMContext):
    await Test.t2.set()
    await bot.send_message(message.chat.id, "Введите название канала")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t2)
async def removeChannel(message: types.Message, state: FSMContext):
    channel = message.text
    #await db.remove_channel_from_news_feed(channel)
    await bot.send_message(message.chat.id, "Канал удалён!")
    await state.finish()


@dp.message_handler(commands=['Каналы'], state=None)
async def getChannels(message: types.Message, state: FSMContext):
    #channels = await db.get_news_channels()
    await bot.send_message(message.chat.id, channels)


@dp.message_handler(commands=['Периоды'], state=None)
async def getPeriod(message: types.Message, state: FSMContext):
    #period = await db.get_news_period()
    await bot.send_message(message.chat.id, period)


@dp.message_handler(commands=['Период'], state=None)
async def addPeriod(message: types.Message, state: FSMContext):
    await Test.t3.set()
    await bot.send_message(message.chat.id, "Введите период")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.t3)
async def setPeriod(message: types.Message, state: FSMContext):
    period = int(message.text)
    #await db.set_news_period(period)
    await bot.send_message(message.chat.id, "Период установлен!")
    await state.finish()


async def loading(state: FSMContext):
    with open('channel_messages.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        message_chid = await state.get_data()
    for i in range(5):
        await bot.send_message(message_chid['message_id'], json_data[i]['message'])
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_url, commands="Новости", state="*")
    dp.register_message_handler(parsing, state=Form.parse)
    dp.register_message_handler(loading, state=Form.load)
