from aiogram.dispatcher.filters.state import State, StatesGroup

class StatesOfMenu(StatesGroup):
    menu = State()
    categories = State()
    list_of_feed_channels = State()
    add_new_category_interring_name_of_category = State()
    my_categories = State()
    editing_category = State()
    test = State()


class NewCategory(StatesGroup):
    add_new_category_interring_name_of_channel = State()
    Waiting = State()


class NewsFeedStates(StatesGroup):
    wait_link = State()



class Form(StatesGroup):
    parse = State()
    load = State() 


class Test(StatesGroup):
    t1 = State()
    t2 = State()
    t3 = State()
    t4 = State()
    t5 = State()
    tt1 = State()
    tt2 = State()
    ttt1 = State()
    ttt2 = State()

