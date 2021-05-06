from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import KeyBoard
from keyboards.inline import InlineKeyBoard
from states.States import StatesOfMenu
from utils.db_api.dp_api import db


@dp.message_handler(commands=['start'], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Привет! (Дописать приветствие)", reply_markup=KeyBoard.start_kb)
    await db.add_new_user()
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
        await bot.send_message(message.from_user.id, "Категории:", reply_markup=KeyBoard.categories_kb)
        await StatesOfMenu.categories.set()
    elif message.text == "Список канало ленты":
        await state.update_data(page=1)  # каждый раз делаем страничку первой, для вывода новостной ленты
        await bot.send_message(message.from_user.id, "Список каналов ленты:", reply_markup= KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Текст", reply_markup= await InlineKeyBoard.create_list_of_feed_channels_kb())
        await StatesOfMenu.list_of_feed_channels.set()
    elif message.text == "Вывести новостную ленту":
        pass
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(state=StatesOfMenu.categories)
async def categories_choice(message: types.Message, state: FSMContext):
    if message.text == "Мои категории":
        await bot.send_message(message.from_user.id, "Мои категории:", reply_markup=KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Текст", reply_markup=InlineKeyBoard.my_categories_kb)
        await StatesOfMenu.my_categories.set()
    elif message.text == "Создать категорию":
        await bot.send_message(message.from_user.id, "Создать категорию:", reply_markup=KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Текст", reply_markup=InlineKeyBoard.new_category_kb)
        await StatesOfMenu.add_new_category.set()
    elif message.text == "Редактирование категорий":
        await bot.send_message(message.from_user.id, "Редактирование категории:", reply_markup=KeyBoard.back_to_menu_kb)
        await bot.send_message(message.from_user.id, "Текст", reply_markup=InlineKeyBoard.editing_category_choice_kb)
        await StatesOfMenu.editing_category.set()
    elif message.text == "Вернуться в меню":
        await state.finish()
        await StatesOfMenu.menu.set()
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(state=StatesOfMenu.all_states)
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
