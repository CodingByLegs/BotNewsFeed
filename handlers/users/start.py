from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
import json
from Parser import parseURL, dump_all_messages
from states.States import Form

from loader import bot
from loader import dp


@dp.message_handler(CommandStart(), state = "*")
async def send_welcome(message: types.Message, state: FSMContext):

    await message.reply("Привет, пользователь")
    await state.finish()


@dp.message_handler(commands=['Новости'], state = None)
async def get_url(message: types.Message):
    await Form.parse.set()
    await bot.send_message(message.chat.id, 'Введите ссылку на канал')


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