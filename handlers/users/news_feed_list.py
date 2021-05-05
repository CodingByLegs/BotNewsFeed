import asyncio
from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.InlineKeyBoard import refresh_list_of_feed_channels_kb
from states.States import NewsFeedStates, StatesOfMenu
from keyboards.inline.callback_dates import channel_callback, page_callback

from loader import bot
from loader import dp
from utils.db_api.dp_api import db


@dp.callback_query_handler(text="add_new_channel", state=StatesOfMenu.list_of_feed_channels)
async def get_link_for_news_feed_channel(call: CallbackQuery):
    await call.answer(cache_time=3)
    await call.message.answer("Введите ссылку на канал в формате t.me/название_канала")
    await NewsFeedStates.wait_link.set()


# перелистывание списка каналов новстной ленты "вперед"
@dp.callback_query_handler(page_callback.filter(rotation="forward"), state=StatesOfMenu.list_of_feed_channels)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) + 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_feed_channels_kb(page))


@dp.callback_query_handler(page_callback.filter(rotation="backward"), state=StatesOfMenu.list_of_feed_channels)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) - 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_feed_channels_kb(page))


@dp.message_handler(text_contains="t.me/", state=NewsFeedStates.wait_link)
async def add_channel_to_news_feed(message: Message, state: FSMContext):
    link = message.text
    if link.startswith("https://t.me/"):
        channel_name = link.partition("https://t.me/")[2]
    elif link.startswith("t.me/"):
        channel_name = link.partition("t.me/")[2]
    else:
        pass  # если не ссылка
    # проверка на наличие такого канала
    await db.add_channel_to_news_feed(channel_name)
    await message.answer("Канал был добавлен!")
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await asyncio.sleep(2)
    await bot.delete_message(message.chat.id, message.message_id + 1)  # удаление последнего отправленного сообщения
    # обновить инлайн клавиатуру
    await StatesOfMenu.list_of_feed_channels.set()
