from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    parse = State()
    loadingh = State()
    show = State()


class Test(StatesGroup):
    t1 = State()
    t2 = State()
