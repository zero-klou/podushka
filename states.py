from aiogram.dispatcher.filters.state import StatesGroup, State

class MainStates(StatesGroup):
    started = State()
    menu = State()
    cart = State()
    search = State()
    feedback = State()
    settings = State()

class MenuStates(StatesGroup):
    choose_product = State()
    select_quantity = State()

class SettingStates(StatesGroup):
    change_number = State()

class Order(StatesGroup):
    delivery_method = State()
    shipping = State()
    payments = State()
    final = State()