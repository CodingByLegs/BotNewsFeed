from aiogram.dispatcher.filters.state import State, StatesGroup

class StatesOfMenu(StatesGroup):
    menu = State()
    categories = State()
    list_of_feed_channels = State()
    add_new_category = State()
    my_categories = State()
    editing_category = State()
    test = State()


class Form(StatesGroup):
    parse = State()
    load = State() 


class Test(StatesGroup):
    t1 = State()
    t2 = State()
    t3 = State()
    t4 = State()
    t5 = State()
