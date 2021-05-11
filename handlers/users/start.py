from datetime import datetime, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

import json
from Parser import parseURL, dump_all_messages, dump_news
from states.States import Form, Test
from loader import client
from loader import bot
from loader import dp
from utils.MyDataJSON import MyDataJSON
from utils.db_api.dp_api import db
import pytz

@dp.message_handler(CommandStart(), state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await db.add_new_user()
    await message.reply("Привет, пользователь")
    timzone = pytz.timezone('Europe/Moscow')
    period = timedelta(minutes=1440)
    date_period: datetime = datetime.utcnow() - period
    x = 10
    messages = client.iter_messages(entity="https://t.me/csgomajor1", limit=10, offset_date=date_period)
    all_messages = []
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)
    try:
        print(x)
        async for message in messages:
            if message.text != "":
                new_message = {'message': message.text,
                               'date': message.date,
                               'message_id': message.id,
                               'current': 'false'}
                all_messages.append(new_message)
        print(x + 1)
    except Exception as e:
        print(x - 1)
        print(e)
    with open('channel_messages.json', 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder, indent=4)
    await state.finish()


@dp.message_handler(commands=['Лента'], state=None)
async def show_news_feed(message: types.Message):
    news_feed_messages: list = await dump_news()
    news_feed_messages_length = len(news_feed_messages)
    lost_news = news_feed_messages[news_feed_messages_length - 1]['lost_news']
    news_feed_messages.pop(news_feed_messages_length - 1)
    print(lost_news)
    for news in news_feed_messages:
        news_date = MyDataJSON(news['date']).date
        # date_to_send = f'''{news_date.day}.{news_date.month} {news_date.hour}:{news_date.minute}\n'''
        date_to_send = f'''{news_date.hour}:{news_date.minute}\n'''
        news_message: str = date_to_send + news['message']
        await bot.send_message(message.chat.id, news_message)


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
    channel = message.text
    if channel.startswith("https://t.me/"):
        channel_name = channel.partition("https://t.me/")[2]
    elif channel.startswith("t.me/"):
        channel_name = channel.partition("t.me/")[2]
    else:
        channel_name = " "
    # await dump_all_messages(url)
    x = 10
    date = MyDataJSON("2021-05-07T16:18:00+00:00")
    date = date.date
    try:
        print(x)
        message_from_channel = client.iter_messages(entity=channel, limit=10, offset_date=date )
        print(x + 1)
    except Exception as e:
        print(x - 1)
        x -= 1
    print(x)


    await state.update_data(message_id=message.chat.id)
    #print(message.chat.id)
    await Form.next()
    tmp = await state.get_data()
    # print(tmp['message_id'])
   # await loading(state)


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


@dp.message_handler(commands=['ДобавитьКанал'], state=None)
async def addChanelIntoCategory1(message: types.Message, state: FSMContext):
    await Test.tt1.set()
    await bot.send_message(message.chat.id, "Введите название категории, в который хотите добавить канал")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.tt1)
async def addChanelIntoCategory2(message: types.Message, state: FSMContext):
    await Test.tt2.set()
    await state.update_data(category_name=message.text)
    await bot.send_message(message.chat.id, "Введите канал, который хотите добавить в категорию: " + message.text)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.tt2)
async def addChanelIntoCategory3(message: types.Message, state: FSMContext):
    tmp = await state.get_data()
    category_name = tmp['category_name']
    channel_name = message.text
    await db.add_channel_to_category(channel_name, category_name)
    await bot.send_message(message.chat.id, 'Канал успешно добавлен')
    await state.finish()


@dp.message_handler(commands=['УдалитьКанал'], state=None)
async def removeChanelFromCategory1(message: types.Message, state: FSMContext):
    await Test.ttt1.set()
    await bot.send_message(message.chat.id, "Введите название категории, из которой вы хотите удалить канал")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.ttt1)
async def removeChanelFromCategory2(message: types.Message, state: FSMContext):
    await Test.ttt2.set()
    await state.update_data(category_name=message.text)
    await bot.send_message(message.chat.id, "Введите канал, который хотите удалить из категории: " + message.text)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Test.ttt2)
async def removeChanelFromCategory3(message: types.Message, state: FSMContext):
    tmp = await state.get_data()
    category_name = tmp['category_name']
    channel_name = message.text
    await db.remove_channel_from_category(channel_name, category_name)
    await bot.send_message(message.chat.id, 'Канал успешно удалён')
    await state.finish()


@dp.message_handler(commands=['1'], state=None)
async def getChannelsFromCategory(message: types.Message, state: FSMContext):
    text = await db.get_category_channels('Тачки')
    await bot.send_message(message.chat.id, text)

@dp.message_handler(commands=['2'], state=None)
async def getUserCategories(message: types.Message, state:FSMContext):
    text = await db.get_user_categories()
    await bot.send_message(message.chat.id, text)

@dp.message_handler(commands=['3'], state=None)
async def addOurCategory(message: types.Message, state:FSMContext):
    category_name = 'Jopa'
    category_channels = ['@dermo','@gavno']
    await db.add_our_category(category_name,category_channels)

@dp.message_handler(commands=['4'], state=None)
async def addChannelsToOurCategory(message: types.Message, state:FSMContext):
    category_name = 'Хуячки'
    category_channels = ['@peins', '@jopa']
    await db.add_channels_to_our_category(category_channels, category_name)

@dp.message_handler(commands=['5'], state=None)
async def addChannelsToOurCategory(message: types.Message, state:FSMContext):
    category_name = 'Jopa'
    category_channels = '@dermo'
    await db.remove_channels_from_our_category(category_channels, category_name)

@dp.message_handler(commands=['6'], state=None)
async def getChannelsOurCategory(message: types.Message, state:FSMContext):
    category_name = 'Jopa'
    text = await db.get_our_category_channels(category_name)
    await bot.send_message(message.chat.id, text)

@dp.message_handler(commands=['7'], state=None)
async def getChannelsOurCategory(message: types.Message, state:FSMContext):
    text = await db.get_our_categories()
    await bot.send_message(message.chat.id, text)

async def loading(state: FSMContext):
    state_data = state.get_data()
    channel_name = state_data['channel_name']
    with open('channel_messages.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

        message_chid = await state.get_data()
    # for i in range(len(json_data)):
    #     await bot.send_message(message_chid['message_id'], json_data[i]['message'])
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_url, commands="Новости", state="*")
    dp.register_message_handler(parsing, state=Form.parse)
    dp.register_message_handler(loading, state=Form.load)
