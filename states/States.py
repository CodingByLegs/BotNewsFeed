from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    parse = State()
    load = State()