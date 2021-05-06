import asyncio
from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.InlineKeyBoard import refresh_list_of_feed_channels_kb, delete_channel_from_news_feed_kb
from states.States import NewsFeedStates, StatesOfMenu
from keyboards.inline.callback_dates import channel_callback, page_callback, action_callback, delete_channel_callback

from loader import bot
from loader import dp
from utils.db_api.dp_api import db


@dp.callback_query_handler(action_callback.filter(action_name="add_new_channel", ),
                           state=StatesOfMenu.list_of_feed_channels)
async def get_link_for_news_feed_channel(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=3)
    await call.message.answer("Введите ссылку на канал в формате t.me/название_канала")
    # запоминаем id сообщения с инлайн кнопками, чтобы поменять его, послое добавления нового канала
    await state.update_data(message_id=call.message.message_id, page=callback_data.get("page"))
    await NewsFeedStates.wait_link.set()


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
    state_data = await state.get_data()  # обновление инлайн клавиатуры
    message_id = state_data['message_id']
    page = state_data['page']
    await bot.edit_message_reply_markup(message_id=message_id,
                                        reply_markup=await refresh_list_of_feed_channels_kb(page))
    await StatesOfMenu.list_of_feed_channels.set()


# перелистывание списка каналов новстной ленты "вперед"
@dp.callback_query_handler(page_callback.filter(rotation="forward"), state=StatesOfMenu.list_of_feed_channels)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) + 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_feed_channels_kb(page))


@dp.callback_query_handler(page_callback.filter(rotation="backward"), state=StatesOfMenu.list_of_feed_channels)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) - 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_feed_channels_kb(page))


@dp.callback_query_handler(channel_callback.filter(), state=StatesOfMenu.list_of_feed_channels)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await state.update_data(message_id=call.message.message_id)  # запоминаем id inline сообщения со спсиком каналов
    channel_name = callback_data.get("channel_name")
    page = callback_data.get("page")
    # отправляем сообщение с клавиаутрой для поддтверждения удаления
    await call.message.answer(f'Удалитиь канал {channel_name}?',
                              reply_markup=await delete_channel_from_news_feed_kb(channel_name, page))


# call_back для нажатия по каналу
@dp.callback_query_handler(delete_channel_callback.filter(), state=StatesOfMenu.list_of_feed_channels)
async def delete_channel(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    channel = callback_data.get("channel_name")
    page = callback_data.get("page")
    state_data = await state.get_data()
    message_id = state_data['message_id']
    if answer == "yes":
        await db.remove_channel_from_news_feed(channel)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=message_id,
                                            reply_markup=await refresh_list_of_feed_channels_kb(page))
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, "Канал удален!")
        await sleep(2)
        await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)




