import asyncio
from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from Parser import dump_all_messages
from handlers.users.start_menu import clear_chat
from keyboards.default import KeyBoard
from keyboards.inline.InlineKeyBoard import refresh_list_of_feed_channels_kb, delete_channel_from_news_feed_kb,\
    refresh_creation_of_categories_kb
from states.States import NewsFeedStates, StatesOfMenu, NewCategory
from keyboards.inline.callback_dates import channel_callback, page_callback, action_callback, delete_channel_callback, \
    special_action_callback

from loader import bot
from loader import dp
from utils.db_api.dp_api import db


@dp.callback_query_handler(special_action_callback.filter(action_name="add_new_channel", ), state=NewCategory.Waiting)
async def get_link(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=3)
    await call.message.answer("Введите ссылку на канал в формате t.me/название_канала")
    await state.update_data(message_id=call.message.message_id,
                            page=callback_data.get("page"),
                            name_of_category=callback_data.get("name_of_channel"),
                            chat_id=call.message.chat.id)
    await state.update_data(last_message_id_to_delete=call.message.message_id)
    await NewCategory.add_new_category_interring_name_of_channel.set()


@dp.message_handler(text_contains="t.me/", state=NewCategory.add_new_category_interring_name_of_channel)
async def add_channel(message: Message, state: FSMContext):
    link = message.text
    if link.startswith("https://t.me/"):
        channel_name = link.partition("https://t.me/")[2]
    elif link.startswith("t.me/"):
        channel_name = link.partition("t.me/")[2]
    else:
        channel_name = " "
    exception = await dump_all_messages(link)
    state_data = await state.get_data()
    if exception:
        await bot.send_message(message.chat.id, "Такого канала не существует или он закрытый")
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.message_id + 1)
    else:
        await db.add_channel_to_category(channel_name, category_name=state_data['name_of_category'])
        await message.answer("Канал был добавлен!")
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.delete_message(message.chat.id, message.message_id)
        await asyncio.sleep(2)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        message_id = state_data['message_id']
        chat_id = state_data['chat_id']
        page = state_data['page']
        await bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=await refresh_creation_of_categories_kb(page, state_data['name_of_category']))
    await NewCategory.Waiting.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=NewCategory.add_new_category_interring_name_of_channel)
async def not_link_add_channel(message: Message, state: FSMContext):
    if message.text == "Вернуться в меню":
        await StatesOfMenu.menu.set()
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
        await clear_chat(message.chat.id, message.message_id, state)
    else:
        await bot.send_message(message.chat.id, "Это не похоже на ссылку!")
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id - 1)
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, message.message_id + 1)
        await NewCategory.Waiting.set()


@dp.callback_query_handler(page_callback.filter(rotation="forward"), state=NewCategory.Waiting)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) + 1
    await call.message.edit_reply_markup(
        reply_markup=await refresh_creation_of_categories_kb(page, callback_data.get('name_of_channel')))


@dp.callback_query_handler(page_callback.filter(rotation="backward"), state=NewCategory.Waiting)
async def show_previous_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) - 1
    await call.message.edit_reply_markup(
        reply_markup=await refresh_creation_of_categories_kb(page, callback_data.get('name_of_channel')))
