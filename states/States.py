from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    parse = State()
    load = State() 


class Test(StatesGroup):
    t1 = State()
    t2 = State()
    t3 = State()
    t4 = State()
    t5 = State()
