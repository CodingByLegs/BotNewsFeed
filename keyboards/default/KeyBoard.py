from aiogram import types


button1 = types.KeyboardButton('Категории')
button2 = types.KeyboardButton('Список канало ленты')
button3 = types.KeyboardButton('Вывести новостную ленту')
start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).add(button3)

button4 = types.KeyboardButton('Мои категории')
button5 = types.KeyboardButton('Создать категорию')
button6 = types.KeyboardButton('Редактирование категорий')
button7 = types.KeyboardButton('Вернуться в меню')
categories_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(button4, button5).add(button6).add(button7)

button8 = types.KeyboardButton('Сутки')
button9 = types.KeyboardButton('Три дня')
button10 = types.KeyboardButton('Неделя')
button11 = types.KeyboardButton('Месяц')
button12 = types.KeyboardButton('Вернуться в меню')
period_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).row(button8, button9).row(button10, button11).add(button12)

button13 = types.KeyboardButton('Вернуться в меню')
back_to_menu_kb = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button13)