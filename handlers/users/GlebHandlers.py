import os

from Parser import dump_news
from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import KeyBoard
from keyboards.inline import InlineKeyBoard
from states.States import StatesOfMenu, NewCategory
from utils.MyDataJSON import MyDataJSON
from utils.db_api.dp_api import db


@dp.message_handler(commands=['start'], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await state.finish()
    hello_word = "Привет! Это твой новостной бот!\n"\
                 "Я умею собирать новости из каналов и отображать их здесь в виде новостной ленты\n" \
                 "Чтобы добавить каналы для новостной ленты нажми на кнопку \"Список каналов ленты\"\n" \
                 "Еще я умею показывать новости по категориям. Есть уже готовые, но ты можешь создать свои!"
    await bot.send_message(message.from_user.id, hello_word, reply_markup=KeyBoard.start_kb)
    await db.add_new_user()
    # создание директории для хранения json файлов пользователя
    path = f'''G:/PyCharmProjects/BotNewsFeed/jsonfiles/{message.from_user.id}'''
    if not os.path.isdir(path):
        os.makedirs(path)
    await StatesOfMenu.menu.set()


@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await StatesOfMenu.test.set()


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.from_user.id, "(Придумать help)")


@dp.message_handler(state=StatesOfMenu.menu)
async def menu_choice(message: types.Message, state: FSMContext):
    if message.text == "Категории":
        await bot.send_message(message.from_user.id, "Управление категориями", reply_markup=KeyBoard.categories_kb)
        await StatesOfMenu.categories.set()
    elif message.text == "Список каналов ленты":
        await state.update_data(page=1)  # каждый раз делаем страничку первой, для вывода новостной ленты
        await bot.send_message(message.from_user.id, "Для удаления канала из списка нажмите по нему", reply_markup=KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Список каналов ленты:",
                               reply_markup=await InlineKeyBoard.create_list_of_feed_channels_kb())
        await StatesOfMenu.list_of_feed_channels.set()
    elif message.text == "Вывести новостную ленту":
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
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(state=StatesOfMenu.categories)
async def categories_choice(message: types.Message, state: FSMContext):
    if message.text == "Мои категории":
        await bot.send_message(message.from_user.id, "Для просмотра новостей из каналов категорий нажимте на них",
                               reply_markup=KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Мои категории:",
                               reply_markup=await InlineKeyBoard.create_my_categories_kb())
        await StatesOfMenu.my_categories.set()
    elif message.text == "Создать категорию":
        user_categories = await db.get_user_categories()
        if user_categories is None or len(user_categories) < 5:
            await bot.send_message(message.from_user.id, "Введите название категории",
                                   reply_markup=KeyBoard.back_to_menu_kb)
            await StatesOfMenu.add_new_category_interring_name_of_category.set()
        else:
            await bot.send_message(message.from_user.id, "Достигнуто максимальное количество допустимых категорий(5)")
    elif message.text == "Редактирование категорий":
        # user_categories =
        if await db.get_user_categories() is not None:
            await bot.send_message(message.from_user.id, "Выбирите категорию для редактирования",
                                   reply_markup=KeyBoard.back_to_menu_kb)
            await bot.send_message(message.from_user.id, "Мои категории:",
                                   reply_markup=await InlineKeyBoard.create_editing_category_kb())
            await StatesOfMenu.editing_category.set()
            # await state.update_data(message_id=message.message_id)
        else:
            await bot.send_message(message.from_user.id,
                                   "У вас ещё нет ни одной созданной кастомной категории для редактирования")
    elif message.text == "Вернуться в меню":
        await state.finish()
        await StatesOfMenu.menu.set()
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(state=StatesOfMenu.add_new_category_interring_name_of_category)
async def add_new_category(message: types.Message, state: FSMContext):
    category_name = message.text
    await db.add_new_category(category_name)
    text_message = f'''Список каналов категории \"{category_name}\":'''
    await bot.send_message(message.from_user.id, text_message,
                           reply_markup=await InlineKeyBoard.create_creation_of_categories_kb(category_name))
    await NewCategory.Waiting.set()
    # if message.text == "Вернуться в меню":
    #     await state.finish()
    #     await StatesOfMenu.menu.set()
    #     await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
    #     await bot.delete_message(message.chat.id, message.message_id) удаление лишних сообщений


# @dp.message_handler(state=NewCategory.all_states)
# async def back_to_menu_from_add_new_category(message: types.Message, state: FSMContext):
#     if message.text == "Вернуться в меню":
#         await state.finish()
#         await StatesOfMenu.menu.set()
#         await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
#
#
# @dp.message_handler(state=StatesOfMenu.all_states)
# async def back_to_menu_from_add_new_category(message: types.Message, state: FSMContext):
#     if message.text == "Вернуться в меню":
#         await state.finish()
#         await StatesOfMenu.menu.set()
#         await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)


@dp.message_handler(state="*")
async def back_to_menu(message: types.Message, state: FSMContext):
    if message.text == "Вернуться в меню":
        await state.finish()
        await StatesOfMenu.menu.set()
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
        # await bot.delete_message(message.chat.id, message.message_id) удаление лишних сообщений


@dp.message_handler(lambda message: message.text.lower() == 'lol', state=StatesOfMenu.test)
async def get_text_messages(message: types.Message):
    if message.text == "Привет":
        await bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        await bot.send_message(message.from_user.id, "Напиши привет")
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
