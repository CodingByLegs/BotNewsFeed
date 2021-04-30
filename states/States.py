from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    parse = State()
    loadingh = State()
    show = State()
