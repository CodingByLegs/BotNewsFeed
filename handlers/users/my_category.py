from aiogram.types import CallbackQuery

from Parser import dump_news
from keyboards.default import KeyBoard
from keyboards.inline.callback_dates import action_callback, category_callback
from loader import bot
from loader import dp
from states.States import StatesOfMenu
from utils.MyDataJSON import MyDataJSON
from utils.db_api.dp_api import db


@dp.callback_query_handler(category_callback.filter(), state=StatesOfMenu.my_categories)
async def show_category(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=3)
    category_name = callback_data['category_name']
    category_feed_messages: list = await dump_news(category_name)
    news_feed_messages_length = len(category_feed_messages)
    lost_news = category_feed_messages[news_feed_messages_length - 1]['lost_news']
    category_feed_messages.pop(news_feed_messages_length - 1)
    for news in category_feed_messages:
        news_date = MyDataJSON(news['date']).date
        # date_to_send = f'''{news_date.day}.{news_date.month} {news_date.hour}:{news_date.minute}\n'''
        date_to_send = f'''{news_date.hour}:{news_date.minute}\n'''
        news_message: str = date_to_send + news['message']
        await bot.send_message(call.message.chat.id, news_message)


@dp.callback_query_handler(action_callback.filter(action_name="back"), state=StatesOfMenu.my_categories)
async def back_from_my_category(call: CallbackQuery):
    await call.answer(cache_time=1)
    for i in range(0, 4):
        await bot.delete_message(call.message.chat.id, call.message.message_id - i)
    await bot.send_message(call.message.chat.id, "Управление категориями", reply_markup=KeyBoard.categories_kb)
    await StatesOfMenu.categories.set()





