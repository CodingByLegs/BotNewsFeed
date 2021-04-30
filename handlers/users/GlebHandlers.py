from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import KeyBoard
#from keyboards.inline
from states.States import States_of_menu


@dp.message_handler(commands=['start'], state="*")
async def welcome(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, "Привет! (Дописать приветствие)", reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
    await States_of_menu.menu.set()


@dp.message_handler(commands="cancel", state="*")
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await States_of_menu.test.set()


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await bot.send_message(message.from_user.id, "(Придумать help)")


@dp.message_handler(state=States_of_menu.menu)
async def menu_choice(message: types.Message, state: FSMContext):
    if message.text == "Категории":
        await bot.send_message(message.from_user.id, "Категории:", reply_markup=KeyBoard.categories_kb)
        await States_of_menu.categories.set()
    elif message.text == "Список канало ленты":
        pass
    elif message.text == "Вывести новостную ленту":
        pass
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(state=States_of_menu.categories)
async def categories_choice(message: types.Message, state: FSMContext):
    if message.text == "Мои категории":
        pass
    elif message.text == "Создать категорию":
        pass
    elif message.text == "Редактирование категорий":
        pass
    elif message.text == "Вернуться в меню":
        await state.finish()
        await States_of_menu.menu.set()
        await bot.send_message(message.from_user.id, "Меню:", reply_markup=KeyBoard.start_kb)
    else:
        await bot.send_message(message.from_user.id, "Нажми на клавиатуру или напиши /info для вызова подсказки")
        return


@dp.message_handler(lambda message: message.text.lower() == 'lol', state=States_of_menu.test)
async def get_text_messages(message: types.Message):
    if message.text == "Привет":
        await bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        await bot.send_message(message.from_user.id, "Напиши привет")
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
