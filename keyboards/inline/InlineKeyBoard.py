from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_of_feed_channels_kb = InlineKeyboardMarkup(
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
            InlineKeyboardButton(text="Добавить новый канал", callback_data="add_new_channel"),
        ]
    ]
)

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