from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_section = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🍴 Подущечная'),
            KeyboardButton(text='🍴 Галиреющка')
        ]
    ],
    resize_keyboard=True
)

start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🍽 Меню')
        ],
        [
            KeyboardButton(text='✍️ Оставить отзыв'),
            KeyboardButton(text='🔎 Поиск')
        ],
        [
            KeyboardButton(text='📞 Наши контакты'),
            KeyboardButton(text='📥 Корзина')
            
        ],
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
sections = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='Тестовая секция'),
            KeyboardButton(text='Тестовая секция 2')
        ],
        [
            KeyboardButton(text='🚖 Оформить заказ')
        ],
        [
            KeyboardButton(text='📥 Корзина'),
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
test_section1_products = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='📥 Корзина'),
            KeyboardButton(text='⏫ Список')
        ],
        [
            KeyboardButton(text='Тестовое блюдо'),
            KeyboardButton(text='Тестовое блюдо 2')
        ],
        [
            KeyboardButton(text='🏠 На главную'),
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
test_section2_products = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='📥 Корзина'),
            KeyboardButton(text='⏫ Список')
        ],
        [
            KeyboardButton(text='Тестовое блюдо 3'),
            KeyboardButton(text='Тестовое блюдо 4')
        ],
        [
            KeyboardButton(text='🏠 На главную'),
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
quantity = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='1'),
            KeyboardButton(text='2'),
            KeyboardButton(text='3')
        ],
        [
            KeyboardButton(text='4'),
            KeyboardButton(text='5'),
            KeyboardButton(text='6')
        ],
        [
            KeyboardButton(text='7'),
            KeyboardButton(text='8'),
            KeyboardButton(text='9')
        ],
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
back = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
settings = ReplyKeyboardMarkup(
    keyboard = 
    [
        [
            KeyboardButton(text='Изменить номер')
        ],
        [
            KeyboardButton(text='🏠 На главную')
        ]
    ],
    resize_keyboard=True
)
send_contact = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text='☎️ Отправить контакт', request_contact=True)
        ],
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
delivery_method = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🚖 Доставка'),
            KeyboardButton(text='🏃 Самовывоз')
        ],
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
shipping = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🏠 На главную'),
            KeyboardButton(text='⬅️ назад')
        ],
        [
            KeyboardButton(text='🗺 Отправить геолокацию', request_location=True)
        ]
    ],
    resize_keyboard=True
)
payments = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='💵 Наличные'),
        ],
        [
            KeyboardButton(text='💳 Payme'),
            KeyboardButton(text='💳 Click')
        ],
        [
            KeyboardButton(text='⬅️ назад')
        ]
    ],
    resize_keyboard=True
)
confirm = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='✅ Заказываю!')
        ],
        [
            KeyboardButton(text='❌ Отменить')
        ]
    ],
    resize_keyboard=True
)
admin_kb = InlineKeyboardMarkup(row_width=2)
admin_kb.insert(InlineKeyboardButton(text='Подтвердить', callback_data='confirmed'))
admin_kb.insert(InlineKeyboardButton(text='Отказать', callback_data='canceled'))