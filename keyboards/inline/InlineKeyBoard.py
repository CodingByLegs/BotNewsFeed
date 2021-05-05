from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_dates import channel_callback, page_callback
from utils.db_api.dp_api import db
from loader import bot
from loader import dp


async def create_list_of_feed_channels_kb():
    list_of_channels: list = await db.get_news_channels()
    print(list_of_channels)
    list_of_feed_channels_kb = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    for channel in list_of_channels:
        count_of_channels += 1
        # создаем кнопки с названием каналов и сразу добавляем их в клавиатуру
        inline_button = InlineKeyboardButton(text=channel, callback_data=channel_callback.new(channel_name=channel))
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
    button_add_channel = InlineKeyboardButton(text="Добавить новый канал", callback_data="add_new_channel")
    list_of_feed_channels_kb.row(button_pages1, button_pages2, button_pages3)
    list_of_feed_channels_kb.add(button_add_channel)

    return list_of_feed_channels_kb


async def refresh_list_of_feed_channels_kb(page: int):
    list_of_channels: list = await db.get_news_channels()
    print(list_of_channels)
    print(page)
    list_of_channels = list_of_channels[8 * (page - 1)::]  # пропускаем по 8 страниц, которые вывели до этого
    print(list_of_channels)
    list_of_feed_channels_kb = InlineKeyboardMarkup(row_width=1)
    count_of_channels = 0
    for channel in list_of_channels:
        count_of_channels += 1
        # создаем кнопки с названием каналов и сразу добавляем их в клавиатуру
        inline_button = InlineKeyboardButton(text=channel, callback_data=channel_callback.new(channel_name=channel))
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

    button_add_channel = InlineKeyboardButton(text="Добавить новый канал", callback_data="add_new_channel")
    list_of_feed_channels_kb.row(button_pages1, button_pages2, button_pages3)
    list_of_feed_channels_kb.add(button_add_channel)
    return list_of_feed_channels_kb


new_category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="back"),
            InlineKeyboardButton(text="1️⃣", callback_data="none"),
            InlineKeyboardButton(text="➡️", callback_data="forward"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 5", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 6", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 7", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 8", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data="back"),
            InlineKeyboardButton(text="1️⃣", callback_data="none"),
            InlineKeyboardButton(text="➡️", callback_data="forward"),
        ],
        [
            InlineKeyboardButton(text="Добавить новый канал", callback_data="add_new_channel"),
        ],
        [
            InlineKeyboardButton(text="Сохранить категорию", callback_data="save"),
        ]
    ]
)

my_categories_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Наша категория 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 5", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 5", callback_data="ДОПИСАТЬ"),
        ]
    ]
)

editing_category_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="back"),
            InlineKeyboardButton(text="1️⃣", callback_data="none"),
            InlineKeyboardButton(text="➡️", callback_data="forward"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 5", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 6", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 7", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Название кананала 8", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="⬅️", callback_data="back"),
            InlineKeyboardButton(text="1️⃣", callback_data="none"),
            InlineKeyboardButton(text="➡️", callback_data="forward"),
        ],
        [
            InlineKeyboardButton(text="Добавить из своих каналов", callback_data="add_from_my_channels"),
        ],
        [
            InlineKeyboardButton(text="Добавить новый канал", callback_data="add_new_channel_to_category"),
        ]
    ]
)

editing_category_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Наша категория 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Наша категория 5", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 1", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 2", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 3", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 4", callback_data="ДОПИСАТЬ"),
        ],
        [
            InlineKeyboardButton(text="Категория пользователя 5", callback_data="ДОПИСАТЬ"),
        ]
    ]
)
