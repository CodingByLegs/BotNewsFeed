from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_dates import channel_callback, page_callback, action_callback, delete_channel_callback, \
    category_callback, special_action_callback, special_page_callback, special_delete_channel_callback, \
    action_callback_with_category, page_callback_with_category, channel_callback_with_category, delete_category_callback
from utils.db_api.dp_api import db
from loader import bot
from loader import dp


async def create_list_of_feed_channels_kb():
    list_of_channels: list = await db.get_news_channels()
    list_of_feed_channels_kb = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    if list_of_channels is not None:
        for channel in list_of_channels:
            count_of_channels += 1
            # создаем кнопки с названием каналов и сразу добавляем их в клавиатуру
            inline_button = InlineKeyboardButton(text=channel,
                                                 callback_data=channel_callback.new(channel_name=channel, page=1))
            list_of_feed_channels_kb.insert(inline_button)
            if count_of_channels == 8:  # не более 8 каналов на одной странице
                break
        button_pages1 = InlineKeyboardButton(text="⏺️ ", callback_data="none")
        button_pages2 = InlineKeyboardButton(text=1, callback_data="none")
        if len(list_of_channels) > 8:
            button_pages3 = InlineKeyboardButton(text="➡️",
                                                 callback_data=page_callback.new(page_number=1, rotation="forward"))
        else:
            button_pages3 = InlineKeyboardButton(text="⏺️",
                                                 callback_data="none")
        list_of_feed_channels_kb.row(button_pages1, button_pages2, button_pages3)
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=action_callback.new(action_name="add_new_channel",
                                                                                page=1))
    list_of_feed_channels_kb.add(button_add_channel)

    return list_of_feed_channels_kb


async def refresh_list_of_feed_channels_kb(page: int):
    list_of_channels: list = await db.get_news_channels()
    page = int(page)
    list_of_channels = list_of_channels[8 * (page - 1)::]  # пропускаем по 8 страниц, которые вывели до этого
    list_of_feed_channels_kb = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    for channel in list_of_channels:
        count_of_channels += 1
        # создаем кнопки с названием каналов и сразу добавляем их в клавиатуру
        inline_button = InlineKeyboardButton(text=channel,
                                             callback_data=channel_callback.new(channel_name=channel, page=page))
        list_of_feed_channels_kb.insert(inline_button)
        if count_of_channels == 8:  # не более 8 каналов на одной странице
            break

    if page > 1:
        button_pages1 = InlineKeyboardButton(text="⬅️", callback_data=page_callback.new(page_number=page,
                                                                                        rotation="backward"))
    else:
        button_pages1 = InlineKeyboardButton(text="⏺️", callback_data="none")

    button_pages2 = InlineKeyboardButton(text=page, callback_data="none")

    if len(list_of_channels) > 8:
        button_pages3 = InlineKeyboardButton(text="➡️", callback_data=page_callback.new(page_number=page,
                                                                                        rotation="forward"))
    else:
        button_pages3 = InlineKeyboardButton(text="⏺️",
                                             callback_data="none")

    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=action_callback.new(action_name="add_new_channel",
                                                                                page=page))
    list_of_feed_channels_kb.row(button_pages1, button_pages2, button_pages3)
    list_of_feed_channels_kb.add(button_add_channel)
    return list_of_feed_channels_kb


async def delete_channel_from_news_feed_kb(channel: str, page):
    delete_channel_kb = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text="да", callback_data=delete_channel_callback.new(answer="yes",
                                                                                           channel_name=channel,
                                                                                           page=page))
    button_no = InlineKeyboardButton(text="нет", callback_data=delete_channel_callback.new(answer="no",
                                                                                           channel_name=channel,
                                                                                           page=page))
    delete_channel_kb.row(button_yes, button_no)
    return delete_channel_kb


async def create_my_categories_kb():
    my_categories_custom: list = await db.get_user_categories()
    my_categories_our: list = await db.get_our_categories()
    my_categories_kb = InlineKeyboardMarkup(row_width=1)
    if my_categories_custom is not None:
        for category in my_categories_custom:
            inline_button = InlineKeyboardButton(text=category,
                                                 callback_data=category_callback.new(category_name=category))
            my_categories_kb.insert(inline_button)
    for category in my_categories_our:
        inline_button = InlineKeyboardButton(text=category,
                                             callback_data=category_callback.new(category_name=category))
        my_categories_kb.insert(inline_button)
    my_categories_kb.add(InlineKeyboardButton(text="Назад",
                                              callback_data=action_callback.new(action_name="back", page=0)))
    return my_categories_kb


async def create_creation_of_categories_kb(category_name: str):
    creation_of_categories_kb = InlineKeyboardMarkup(row_width=1)
    button_pages1 = InlineKeyboardButton(text="⏺️ ", callback_data="none")
    button_pages2 = InlineKeyboardButton(text=1, callback_data="none")
    button_pages3 = InlineKeyboardButton(text="➡️",
                                         callback_data=special_page_callback.new(page_number=1, rotation="forward",
                                                                                 name_of_channel=category_name))
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=special_action_callback.new(action_name="add_new_channel",
                                                                                        page=1,
                                                                                        name_of_channel=category_name))
    creation_of_categories_kb.row(button_pages1, button_pages2, button_pages3)
    creation_of_categories_kb.add(button_add_channel)
    return creation_of_categories_kb


async def refresh_creation_of_categories_kb(page: int, category_name: str):
    channels_of_category_name: list = await db.get_category_channels(category_name=category_name)
    page = int(page)
    channels_of_category_name = channels_of_category_name[
                                8 * (page - 1)::]  # пропускаем по 8 страниц, которые вывели до этого
    creation_of_categories_kb = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    for channel in channels_of_category_name:
        count_of_channels += 1
        # создаем кнопки с названием каналов и сразу добавляем их в клавиатуру
        inline_button = InlineKeyboardButton(text=channel,
                                             callback_data=channel_callback.new(channel_name=channel, page=page))
        creation_of_categories_kb.insert(inline_button)
        if count_of_channels == 8:  # не более 8 каналов на одной странице
            break
    if page > 1:
        button_pages1 = InlineKeyboardButton(text="⬅️", callback_data=special_page_callback.new(page_number=page,
                                                                                                rotation="backward",
                                                                                                name_of_channel=category_name))
    else:
        button_pages1 = InlineKeyboardButton(text="⏺️", callback_data="none")
    button_pages2 = InlineKeyboardButton(text=page, callback_data="none")
    if len(channels_of_category_name) > 8:
        button_pages3 = InlineKeyboardButton(text="➡️",
                                             callback_data=special_page_callback.new(page_number=page,
                                                                                     rotation="forward",
                                                                                     name_of_channel=category_name))
    else:
        button_pages3 = InlineKeyboardButton(text="⏺️",
                                             callback_data="none")
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=special_action_callback.new(action_name="add_new_channel",
                                                                                        page=page,
                                                                                        name_of_channel=category_name))
    creation_of_categories_kb.row(button_pages1, button_pages2, button_pages3)
    creation_of_categories_kb.add(button_add_channel)
    return creation_of_categories_kb


async def create_editing_category_kb():
    custom_categories: list = await db.get_user_categories()
    editing_category_choice_kb = InlineKeyboardMarkup(row_width=1)
    if custom_categories is not None:
        for category in custom_categories:
            inline_button = InlineKeyboardButton(text=category, callback_data=category_callback.new(category_name=category))
            editing_category_choice_kb.insert(inline_button)
        editing_category_choice_kb.add(InlineKeyboardButton(text="Назад",
                                                            callback_data=action_callback.new(action_name="back",
                                                                                              page=0)))
    return editing_category_choice_kb


async def create_list_of_channels_of_category_kb(category_name: str):
    list_of_channels: list = await db.get_category_channels(category_name)
    list_of_channels_of_category = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    if list_of_channels is not None:
        for channel in list_of_channels:
            count_of_channels += 1
            inline_button = InlineKeyboardButton(text=channel,
                                                 callback_data=channel_callback_with_category.new(channel_name=channel,
                                                                                                  category_name=category_name,
                                                                                                  page=1))
            list_of_channels_of_category.insert(inline_button)
            if count_of_channels == 8:
                break
        button_pages1 = InlineKeyboardButton(text="⏺️ ", callback_data="none")
        button_pages2 = InlineKeyboardButton(text=1, callback_data="none")
        if len(list_of_channels) > 8:
            button_pages3 = InlineKeyboardButton(text="➡️",
                                                 callback_data=page_callback_with_category.new(page_number=1,
                                                                                               rotation="forward",
                                                                                               category_name=category_name))
        else:
            button_pages3 = InlineKeyboardButton(text="⏺️",
                                                 callback_data="none")
        list_of_channels_of_category.row(button_pages1, button_pages2, button_pages3)
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=
                                              action_callback_with_category.new(action_name="add_new_channel", page=1,
                                                                                category_name=category_name))
    list_of_channels_of_category.add(button_add_channel)
    list_of_channels_of_category.add(InlineKeyboardButton(text="Удалить категорию", callback_data=
                                                          delete_category_callback.new(category_name=category_name)))
    list_of_channels_of_category.add(InlineKeyboardButton(text="Назад", callback_data=
                                                          action_callback_with_category.new(action_name="back",
                                                                                            page=0,
                                                                                            category_name=category_name)
                                                          ))
    return list_of_channels_of_category


async def refresh_list_of_channels_of_category_kb(category_name: str, page: int):
    list_of_channels: list = await db.get_category_channels(category_name)
    page = int(page)
    list_of_channels = list_of_channels[8 * (page - 1)::]
    list_of_channels_of_category = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    for channel in list_of_channels:
        count_of_channels += 1
        inline_button = InlineKeyboardButton(text=channel,
                                             callback_data=channel_callback_with_category.new(channel_name=channel,
                                                                                              category_name=category_name,
                                                                                              page=1))
        list_of_channels_of_category.insert(inline_button)
        if count_of_channels == 8:
            break
    if page > 1:
        button_pages1 = InlineKeyboardButton(text="⬅️", callback_data=page_callback_with_category.new(page_number=page,
                                                                                                      rotation="backward",
                                                                                                      category_name=category_name))
    else:
        button_pages1 = InlineKeyboardButton(text="⏺️", callback_data="none")
    button_pages2 = InlineKeyboardButton(text=page, callback_data="none")
    if len(list_of_channels) > 8:
        button_pages3 = InlineKeyboardButton(text="➡️", callback_data=page_callback_with_category.new(page_number=page,
                                                                                                      rotation="forward",
                                                                                                      category_name=category_name))
    else:
        button_pages3 = InlineKeyboardButton(text="⏺️",
                                             callback_data="none")
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал",
                                              callback_data=action_callback_with_category.new(
                                                  action_name="add_new_channel", page=1,
                                                  category_name=category_name))
    list_of_channels_of_category.row(button_pages1, button_pages2, button_pages3)
    list_of_channels_of_category.add(button_add_channel)
    list_of_channels_of_category.add(InlineKeyboardButton(text="Удалить категорию",
                                                          callback_data=delete_category_callback.new(
                                                              category_name=category_name)))
    list_of_channels_of_category.add(InlineKeyboardButton(text="Назад", callback_data=
                                                          action_callback_with_category.new(action_name="back",
                                                                                            page=0,
                                                                                            category_name=category_name)
                                                          ))

    return list_of_channels_of_category


async def delete_channel_or_category_kb(category_name: str, channel='\n', page=-1):
    delete_channel_from_category = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text="да",
                                      callback_data=special_delete_channel_callback.new(answer="yes",
                                                                                        channel_name=channel,
                                                                                        category_name=category_name,
                                                                                        page=page))
    button_no = InlineKeyboardButton(text="нет",
                                     callback_data=special_delete_channel_callback.new(answer="no",
                                                                                       channel_name=channel,
                                                                                       category_name=category_name,
                                                                                       page=page))
    delete_channel_from_category.row(button_yes, button_no)
    return delete_channel_from_category
