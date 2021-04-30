from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    parse = State()
    load = State()


class Test(StatesGroup):
    t1 = State()
    t2 = State()
