import asyncio
from asyncio import sleep

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.InlineKeyBoard import refresh_list_of_feed_channels_kb, delete_channel_from_news_feed_kb,\
    refresh_creation_of_categories_kb, create_list_of_channels_of_category_kb, refresh_list_of_channels_of_category_kb,\
    delete_channel_or_category_kb
from states.States import NewsFeedStates, StatesOfMenu, NewCategory, EditingCategory
from keyboards.inline.callback_dates import channel_callback, page_callback, action_callback, delete_channel_callback, \
    special_action_callback, category_callback, special_delete_channel_callback, special_page_callback,\
    action_callback_with_category, page_callback_with_category, channel_callback_with_category, delete_category_callback

from loader import bot
from loader import dp
from utils.db_api.dp_api import db


@dp.callback_query_handler(category_callback.filter(), state=StatesOfMenu.editing_category)
async def editing_category(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    category_name = callback_data.get("category_name")
    text_message1 = "Для удаления канала из категории нажмите по нему\n"
    text_message2 = f'''Список каналов категории \"{category_name}\":'''
    await call.message.answer(text_message1)
    await call.message.answer(text_message2, reply_markup=await create_list_of_channels_of_category_kb(category_name))
    await EditingCategory.editing_category.set()


@dp.callback_query_handler(action_callback_with_category.filter(action_name="add_new_channel"), state=StatesOfMenu.editing_category)
async def get_link_for_new_channel(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=3)
    await call.message.answer("Введите ссылку на канал в формате t.me/название_канала")
    await state.update_data(message_id=call.message.message_id,
                            page=callback_data.get("page"),
                            chat_id=call.message.chat.id,
                            category_name=callback_data.get("category_name"))
    await EditingCategory.wait_link.set()


@dp.message_handler(text_contains="t.me/", state=EditingCategory.wait_link)
async def add_new_channel(message: Message, state: FSMContext):
    link = message.text
    if link.startswith("https://t.me/"):
        channel_name = link.partition("https://t.me/")[2]
    elif link.startswith("t.me/"):
        channel_name = link.partition("t.me/")[2]
    else:
        pass
    state_data = await state.get_data()
    await db.add_channel_to_category(channel_name, state_data['category_name'])
    await message.answer("Канал был добавлен!")
    await bot.delete_message(message.chat.id, message.message_id - 1)
    await bot.delete_message(message.chat.id, message.message_id)
    await asyncio.sleep(2)
    await bot.delete_message(message.chat.id, message.message_id + 1)
    message_id = state_data['message_id']
    page = state_data['page']
    chat_id = state_data['chat_id']
    category_name = state_data['category_name']
    await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=await refresh_list_of_channels_of_category_kb(category_name, page))
    await StatesOfMenu.editing_category.set()


@dp.callback_query_handler(page_callback_with_category.filter(rotation="forward"), state=StatesOfMenu.editing_category)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) + 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_channels_of_category_kb(callback_data.get("category_name"), page))


@dp.callback_query_handler(page_callback_with_category.filter(rotation="backward"), state=StatesOfMenu.editing_category)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page_number")) - 1
    await call.message.edit_reply_markup(reply_markup=await refresh_list_of_channels_of_category_kb(callback_data.get("category_name"), page))


@dp.callback_query_handler(channel_callback_with_category.filter(), state=StatesOfMenu.editing_category)
async def show_next_channels_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await state.update_data(message_id=call.message.message_id)
    channel_name = callback_data.get("channel_name")
    category_name = callback_data.get("category_name")
    page = callback_data.get("page")
    await call.message.answer(f'Удалитиь канал {channel_name} из категории {category_name}?',
                              reply_markup=await delete_channel_or_category_kb(category_name, channel_name, page))


@dp.callback_query_handler(special_delete_channel_callback.filter(), state=StatesOfMenu.editing_category)
async def delete_channel(call: CallbackQuery, callback_data: dict, state: FSMContext):
    answer = callback_data.get("answer")
    category_name = callback_data.get("category_name")
    channel = callback_data.get("channel_name")
    page = callback_data.get("page")
    state_data = await state.get_data()
    message_id = state_data['message_id']
    if answer == "yes":
        await db.remove_channel_from_category(channel, category_name)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=message_id,
                                            reply_markup=await refresh_list_of_channels_of_category_kb(category_name, page))
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, "Канал удален!")
        await sleep(2)
        await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)


# @dp.callback_query_handler(delete_category_callback.filter(), state=StatesOfMenu.editing_category)
# async def delete_category(call: CallbackQuery, callback_data: dict, state: FSMContext):

