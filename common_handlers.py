from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
import messages
import keyboards
import requests
from states import MainStates, MenuStates, SettingStates, Order
from config import load_config
from product_cards import products
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

config = load_config('bot.ini')

bot = Bot(token=config.tg_bot.token)

class User():
    def __init__(self, username, user_id, phone=None, section=None):
        self.username = username
        self.user_id = user_id
        self.phone = phone
        self.section = section
        self.cart = {
            'names': [],
            'prices': [],
            'quantitys': [],
            'current_name': None,#отслеживаем последнее выбранное блюдо
            'current_price': None
        }
        self.order = {
            'delivery_method': None,
            'address': None,
            'payment_method': None,
            'order_list': '',
            'final_check': '',
            'order_complete': False
        }

order_index = [0]
users = []

def get_user_index(username):
    for user in users:
        if user.username == username:
            return users.index(user)
    return None

async def process_start(msg: types.Message, state: FSMContext):
    if get_user_index(msg.from_user.username) == None:
        users.append(User(msg.from_user.username, msg.from_user.id))
    await msg.answer('Выберите компанию', reply_markup=keyboards.main_section)

async def back_to_process_start(msg: types.Message, state: FSMContext):
    await msg.answer('Выберите компанию', reply_markup=keyboards.main_section)
    await state.finish()

async def process_cmd_start(msg: types.Message, state: FSMContext):
    section = ''.join(list(msg.text)[2:])
    users[get_user_index(msg.from_user.username)].section = section

    await msg.answer(f'''Assalomu aleykum {msg.from_user.username}
McBurgers Botiga Xush kelibsiz!
Здравствуйте {msg.from_user.username} !
Добро пожаловать в McBurgers Bot!''')
    await msg.answer(messages.start, reply_markup=keyboards.start)
    await MainStates.first()

async def back_to_start(msg: types.Message, state: FSMContext):
    await msg.answer(messages.start, reply_markup=keyboards.start)
    await MainStates.first()

async def echo(msg: types.Message, state: FSMContext):
    await msg.answer(messages.dumbass)

async def process_menu(msg: types.Message, state:FSMContext):
    await MainStates.menu.set()
    await msg.answer(messages.choose_section, reply_markup=keyboards.sections)

# Выбираем раздел с едой
async def process_section_test1(msg: types.Message, state: FSMContext):
    await MenuStates.choose_product.set() 
    await msg.answer(messages.choose_product, reply_markup=keyboards.test_section1_products)

async def process_section_test2(msg: types.Message, state: FSMContext):
    await MenuStates.choose_product.set() 
    await msg.answer(messages.choose_product, reply_markup=keyboards.test_section2_products)

# Выбираем продукт
async def process_product(msg: types.Message, state: FSMContext):
    product_name = msg.text
    product_dict = None

    for value in products.values():
        if value['button'] == product_name:
            product_dict = value
            break

    users[get_user_index(msg.from_user.username)].cart['current_name'] = product_dict['name']
    users[get_user_index(msg.from_user.username)].cart['current_price'] = product_dict['price']

    await msg.answer_photo(photo=product_dict['path'], caption=f"{product_dict['name']}\n\n{product_dict['composition']}\n\n{product_dict['price']}")
    await msg.answer(messages.choose_quantity, reply_markup=keyboards.quantity)

    await MenuStates.select_quantity.set()

async def process_product_showall(msg: types.Message, state: FSMContext):
    for product_dict in products.values():
        await msg.answer_photo(photo=product_dict['path'], caption=f"{product_dict['name']}\n\n{product_dict['composition']}\n\n{product_dict['price']}")


# Количество продукта
async def process_quantity(msg: types.Message, state: FSMContext):
    await msg.answer(messages.added_to_cart)
    users[get_user_index(msg.from_user.username)].cart['names'].append(users[get_user_index(msg.from_user.username)].cart['current_name'])
    users[get_user_index(msg.from_user.username)].cart['prices'].append(users[get_user_index(msg.from_user.username)].cart['current_price'])
    users[get_user_index(msg.from_user.username)].cart['quantitys'].append(msg.text)
    await msg.answer(messages.want_more, reply_markup=keyboards.sections)

    await MainStates.menu.set()

# Корзина
async def process_to_cart(msg: types.Message, state: FSMContext):
    if users[get_user_index(msg.from_user.username)].phone == None:
        await msg.answer('Сначала укажите свой номер телефона')

        await MainStates.settings.set()
        await msg.answer('⚙️ Настройки', reply_markup=keyboards.settings)
        return

    try: #проверем, пустой ли массив с продуктами cart['names']
        users[get_user_index(msg.from_user.username)].cart['names'][0] == None
    except IndexError: 
        await msg.answer('Ваша корзина пуста')
        return

    await MainStates.cart.set()
    users[get_user_index(msg.from_user.username)].order['order_complete'] = True

    total_cost = 0
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    users[get_user_index(msg.from_user.username)].order['order_list'] = ''

    for i in range(len(users[get_user_index(msg.from_user.username)].cart['names'])):
        price = ''
        for s in list(users[get_user_index(msg.from_user.username)].cart['prices'][i]):
            try: #отсеиваем из строки всё, кроме числа
                int(s)
            except ValueError:
                continue

            price += s

        name = users[get_user_index(msg.from_user.username)].cart['names'][i]
        quantity = users[get_user_index(msg.from_user.username)].cart['quantitys'][i]
        cost = int(price) * int(quantity)
        
        users[get_user_index(msg.from_user.username)].order['order_list'] += f'📥 Корзина\n{name}\n{quantity} x {price} = {cost}\n\n'

        total_cost += cost

        keyboard.add(f'❌ {name}')

    keyboard.add('⬅️ назад', '🔄 Очистить')
    keyboard.add('🚖 Оформить заказ')
    users[get_user_index(msg.from_user.username)].order['keyboard'] = keyboard

    users[get_user_index(msg.from_user.username)].order['order_list'] += str(total_cost)

    await msg.answer(users[get_user_index(msg.from_user.username)].order['order_list'], reply_markup=keyboard)

    #удалить из корзины
async def delete_from_cart(msg: types.Message, state: FSMContext):
    product_name = ''.join(list(msg.text)[2:])

    index_in_cart = users[get_user_index(msg.from_user.username)].cart['names'].index(product_name)
#удаляем имя, число и стоимтость продукта
    users[get_user_index(msg.from_user.username)].cart['names'].pop(index_in_cart)
    users[get_user_index(msg.from_user.username)].cart['prices'].pop(index_in_cart)
    users[get_user_index(msg.from_user.username)].cart['quantitys'].pop(index_in_cart)
    users[get_user_index(msg.from_user.username)].order['order_list'] = ''

    try: #проверем, пустой ли массив с продуктами cart['names']
        users[get_user_index(msg.from_user.username)].cart['names'][0] == None
    except IndexError: 
        await msg.answer(messages.start, reply_markup=keyboards.start)
        await MainStates.first()
        return

    total_cost = 0
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(len(users[get_user_index(msg.from_user.username)].cart['names'])):
        price = ''
        for s in list(users[get_user_index(msg.from_user.username)].cart['prices'][i]):
            try: #отсеиваем из строки всё, кроме числа
                int(s)
            except ValueError:
                continue

            price += s

        name = users[get_user_index(msg.from_user.username)].cart['names'][i]
        quantity = users[get_user_index(msg.from_user.username)].cart['quantitys'][i]
        cost = int(price) * int(quantity)
            
        users[get_user_index(msg.from_user.username)].order['order_list'] += f'📥 Корзина\n{name}\n{quantity} x {price} = {cost}\n\n'

        total_cost += cost

        keyboard.add(f'❌ {name}')

    keyboard.add('⬅️ назад', '🔄 Очистить')
    keyboard.add('🚖 Оформить заказ')
    users[get_user_index(msg.from_user.username)].order['keyboard'] = keyboard

    users[get_user_index(msg.from_user.username)].order['order_list'] += str(total_cost)
    await msg.answer(users[get_user_index(msg.from_user.username)].order['order_list'], reply_markup=keyboard)

    #удаляем всё из корзины
async def delete_all(msg: types.Message, state: FSMContext):
    users[get_user_index(msg.from_user.username)].cart['names'].clear()
    users[get_user_index(msg.from_user.username)].cart['prices'].clear()
    users[get_user_index(msg.from_user.username)].cart['quantitys'].clear()

    await msg.answer(messages.start, reply_markup=keyboards.start)
    await MainStates.first()

#поиск
async def search_section(msg: types.Message, state: FSMContext):
    await MainStates.search.set()
    await msg.answer(messages.search, reply_markup=keyboards.back)

async def search(msg: types.Message, state: FSMContext):
    for product in products.values():
        if msg.text.lower() in product['name'].lower():
            if product['section'] == 'Тестовая секция':
                await MenuStates.choose_product.set() 
                await msg.answer(messages.choose_product, reply_markup=keyboards.test_section1_products)
                return
            elif product['section'] == 'тестовая секция 2':
                await MenuStates.choose_product.set() 
                await msg.answer(messages.choose_product, reply_markup=keyboards.test_section2_products)
                return
    await msg.answer(messages.not_found)

#контакты
async def show_contacts(msg: types.Message, state: FSMContext):
    await msg.answer_location(latitude=39.71175537001076, longitude=66.89248103446289)

#отзыв
async def send_feedback(msg: types.Message, state: FSMContext):
    await MainStates.feedback.set()

    await msg.answer(messages.feedback, reply_markup=keyboards.back)

async def fetch_feedback(msg: types.Message, state: FSMContext):
    id_group = None
    if users[get_user_index(msg.from_user.username)].section == 'Подущечная':
        id_group = -1001166794975
    else:
        id_group = -1001216284678

    await bot.send_message(id_group, text=f'{msg.from_user.first_name} {msg.from_user.last_name} - отзыв.\n{msg.text}')

    await msg.answer(messages.thx_feedback)

    await msg.answer(messages.start, reply_markup=keyboards.start)
    await MainStates.first()

#настройки
async def open_settings(msg: types.Message, state: FSMContext):
    await MainStates.settings.set()

    await msg.answer(msg.text, reply_markup=keyboards.settings)

async def change_number(msg: types.Message, state: FSMContext):
    await SettingStates.change_number.set()

    await msg.answer('📱 Для продолжения!\nотправьте свой контакт',
    reply_markup=keyboards.send_contact)

async def fetch_number(msg: types.Message, state: FSMContext):
    users[get_user_index(msg.from_user.username)].phone = msg.contact.phone_number

    await msg.answer(messages.start, reply_markup=keyboards.start)
    await MainStates.first()

async def back_to_num_section(msg: types.Message, state: FSMContext):
    await MainStates.settings.set()
    
    await msg.answer('⚙️ Настройки', reply_markup=keyboards.settings)

#оформляем заказ
async def make_order(msg: types.Message, state: FSMContext):
    if users[get_user_index(msg.from_user.username)].phone == None:
        await msg.answer('Сначала укажите свой номер телефона')

        await MainStates.settings.set()
        await msg.answer('⚙️ Настройки', reply_markup=keyboards.settings)
        return
    try: #проверем, пустой ли массив с продуктами cart['names']
        users[get_user_index(msg.from_user.username)].cart['names'][0] == None
    except IndexError: 
        await msg.answer('Ваша корзина пуста')
        return

    if users[get_user_index(msg.from_user.username)].order['order_complete']:
        await Order.first()
        await msg.answer(messages.choose_delivery, reply_markup=keyboards.delivery_method)
    else:
        print('Чё, сука?!!')
        total_cost = 0
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        users[get_user_index(msg.from_user.username)].order['order_list'] = ''

        for i in range(len(users[get_user_index(msg.from_user.username)].cart['names'])):
            price = ''
            for s in list(users[get_user_index(msg.from_user.username)].cart['prices'][i]):
                try: #отсеиваем из строки всё, кроме числа
                    int(s)
                except ValueError:
                    continue

                price += s

            name = users[get_user_index(msg.from_user.username)].cart['names'][i]
            quantity = users[get_user_index(msg.from_user.username)].cart['quantitys'][i]
            cost = int(price) * int(quantity)
            
            users[get_user_index(msg.from_user.username)].order['order_list'] += f'📥 Корзина\n{name}\n{quantity} x {price} = {cost}\n\n'

            total_cost += cost

            keyboard.add(f'❌ {name}')

        keyboard.add('⬅️ назад', '🔄 Очистить')
        keyboard.add('🚖 Оформить заказ')
        users[get_user_index(msg.from_user.username)].order['keyboard'] = keyboard

        users[get_user_index(msg.from_user.username)].order['order_list'] += str(total_cost)

        await Order.first()
        await msg.answer(messages.choose_delivery, reply_markup=keyboards.delivery_method)


async def back_to_cart(msg: types.Message, state: FSMContext):
    await MainStates.cart.set()
    await msg.answer(users[get_user_index(msg.from_user.username)].order['order_list'], reply_markup=users[get_user_index(msg.from_user.username)].order['keyboard'])

async def pickup(msg: types.Message, state: FSMContext):
    await Order.payments.set()

    users[get_user_index(msg.from_user.username)].order['delivery_method'] = ''.join(list(msg.text)[2:])
    users[get_user_index(msg.from_user.username)].order['address'] = 'Самовывоз'
    
    await msg.answer(messages.choose_payments, reply_markup=keyboards.payments)
    

async def send_address(msg: types.Message, state: FSMContext):
    await Order.shipping.set()

    users[get_user_index(msg.from_user.username)].order['delivery_method'] = ''.join(list(msg.text)[2:])
    await msg.answer(messages.location, reply_markup=keyboards.shipping)

async def back_to_del_method(msg: types.Message, state: FSMContext):
    await Order.first()
    await msg.answer(messages.choose_delivery, reply_markup=keyboards.delivery_method)

async def fetch_address(msg: types.Message, state: FSMContext):
    if not msg.location:
        users[get_user_index(msg.from_user.username)].order['address'] = msg.text
    else:
        users[get_user_index(msg.from_user.username)].order['address'] = (msg.location.latitude, msg.location.longitude)

    await msg.answer(messages.choose_payments, reply_markup=keyboards.payments)

    await Order.payments.set()

async def fetch_payment_method(msg: types.Message, state: FSMContext):
    users[get_user_index(msg.from_user.username)].order['payment_method'] = ''.join(list(msg.text)[2:])
    order_index[0] += 1
    message = f"✅ Ваш заказ: #{order_index[0]}\n💳Способ оплаты: {users[get_user_index(msg.from_user.username)].order['payment_method']}\n📞 Телефон: {users[get_user_index(msg.from_user.username)].phone}\n📝Тип заказа: {users[get_user_index(msg.from_user.username)].order['delivery_method']}\n🏠Адрес:{users[get_user_index(msg.from_user.username)].order['address']}\n\n{users[get_user_index(msg.from_user.username)].order['order_list']}"
    users[get_user_index(msg.from_user.username)].order['final_check'] = message
    
    await msg.answer(message)
    await msg.answer(messages.confirm, reply_markup=keyboards.confirm)

    await Order.final.set()

#подтверждение или отмена
async def cancel_order(msg: types.Message, state: FSMContext):
    await msg.answer(messages.choose_payments, reply_markup=keyboards.payments)
    await Order.payments.set()

async def confirm_order(msg: types.Message, state: FSMContext):
    user = users[get_user_index(msg.from_user.username)]
    id_group = None
    if user.section == 'Подущечная':
        id_group = -1001166794975
    else:
        id_group = -1001216284678

    await bot.send_message(id_group, f"{msg.from_user.username}\n{msg.from_user.first_name} {msg.from_user.last_name}\n{user.order['final_check']}", reply_markup=keyboards.admin_kb)

    user.cart['names'] = []
    user.cart['quantitys'] = []
    user.cart['prices'] = []
    user.cart['current_name'] = None
    user.cart['current_price'] = None

    user.order['delivery_method'] = None
    user.order['address'] = None
    user.order['payment_method'] = None
    user.order['order_list'] = ''
    user.order['final_check'] = ''


    await msg.answer(messages.confirmed, reply_markup=keyboards.start)
    await MainStates.started.set()

async def confirmed_order(callback_query: types.CallbackQuery):
    await callback_query.answer(text="Заказ принят, перезвоните клиенту!", show_alert=True)
    message = callback_query.message['text']
    index_of_n = message.find('\n')
    username = message[:index_of_n]

    await bot.send_message(users[get_user_index(username)].user_id, 'Ваш заказ подтверждён! Ожидайте звонка оператора.')

async def canceled_order(callback_query: types.CallbackQuery):
    await callback_query.answer(text="В заказе отказано, перезвоните клиенту!", show_alert=True)
    message = callback_query.message['text']
    index_of_n = message.find('\n')
    username = message[:index_of_n]

    await bot.send_message(users[get_user_index(username)].user_id, 'Ваш заказ отклонён! Ожидайте звонка оператора.')


def register_handlers_common(dp: Dispatcher):
    dp.register_callback_query_handler(confirmed_order, text='confirmed', state='*')
    dp.register_callback_query_handler(canceled_order, text='canceled', state='*')

    dp.register_message_handler(process_start, commands=['start'], state=None)
    dp.register_message_handler(back_to_process_start, Text(contains='назад', ignore_case=True), state=MainStates.started)

    dp.register_message_handler(process_cmd_start, Text(startswith='🍴'), state=None)
    
    dp.register_message_handler(process_to_cart, Text(contains='корзина', ignore_case=True), state='*')
    dp.register_message_handler(make_order, Text(contains='оформить заказ', ignore_case=True), state=MainStates.cart)
    dp.register_message_handler(pickup, Text(contains='самовывоз', ignore_case=True), state=Order.delivery_method)
    dp.register_message_handler(send_address, Text(contains='доставка', ignore_case=True), state=Order.delivery_method)
    dp.register_message_handler(back_to_start, Text(contains='на главную', ignore_case=True), state=Order.shipping)
    dp.register_message_handler(back_to_del_method, Text(contains='назад', ignore_case=True), state=Order.shipping)
    dp.register_message_handler(fetch_address, state=Order.shipping, content_types=[ContentType.LOCATION, ContentType.TEXT])

    dp.register_message_handler(back_to_del_method, Text(contains='назад', ignore_case=True), state=Order.payments)
    dp.register_message_handler(back_to_cart, Text(contains='назад', ignore_case=True), state=Order.delivery_method)


    

    dp.register_message_handler(fetch_payment_method, state=Order.payments)

    dp.register_message_handler(cancel_order, Text(contains='отменить', ignore_case=True), state=Order.final)
    dp.register_message_handler(confirm_order, Text(contains='заказываю!', ignore_case=True), state=Order.final)

    dp.register_message_handler(process_menu, Text(contains='Меню', ignore_case=True), state=MainStates.started)

    dp.register_message_handler(process_section_test1, Text(equals='Тестовая секция'), state=MainStates.menu)
    dp.register_message_handler(process_section_test2, Text(equals='Тестовая секция 2'), state=MainStates.menu)
    dp.register_message_handler(back_to_start, Text(contains='назад', ignore_case=True), state=MainStates.menu)
    dp.register_message_handler(make_order, Text(contains='оформить заказ', ignore_case=True), state=MainStates.menu)
    dp.register_message_handler(back_to_start, Text(contains='на главную', ignore_case=True), state=MenuStates.choose_product)
    dp.register_message_handler(process_menu, Text(contains='назад', ignore_case=True), state=MenuStates.choose_product)


    dp.register_message_handler(process_product_showall, Text(contains='Список', ignore_case=True), state=MenuStates.choose_product)
    dp.register_message_handler(process_product, state=MenuStates.choose_product)

    dp.register_message_handler(process_menu, Text(contains='назад', ignore_case=True), state=MenuStates.select_quantity)
    dp.register_message_handler(process_quantity, state=MenuStates.select_quantity)

    dp.register_message_handler(delete_from_cart, Text(startswith='❌'), state=MainStates.cart)
    dp.register_message_handler(delete_all, Text(startswith='🔄'), state=MainStates.cart)
    dp.register_message_handler(process_menu, Text(contains='назад', ignore_case=True), state=MainStates.cart)

    dp.register_message_handler(back_to_start, Text(contains='назад', ignore_case=True), state=MainStates.search)
    dp.register_message_handler(search_section, Text(contains='поиск', ignore_case=True), state=MainStates.started)
    dp.register_message_handler(search, state=MainStates.search)

    dp.register_message_handler(show_contacts, Text(contains='наши контакты', ignore_case=True), state=MainStates.started)

    dp.register_message_handler(send_feedback, Text(contains='оставить отзыв', ignore_case=True), state=MainStates.started)
    dp.register_message_handler(back_to_start, Text(contains='назад', ignore_case=True), state=MainStates.feedback)
    dp.register_message_handler(fetch_feedback, state=MainStates.feedback, content_types=ContentType.TEXT)

    dp.register_message_handler(open_settings, Text(contains='настройки', ignore_case=True), state=MainStates.started)
    dp.register_message_handler(back_to_start, Text(contains='на главную', ignore_case=True), state=MainStates.settings)
    dp.register_message_handler(change_number, Text(contains='изменить номер', ignore_case=True), state=MainStates.settings)
    dp.register_message_handler(fetch_number, state=SettingStates.change_number, content_types=ContentType.CONTACT)
    dp.register_message_handler(back_to_num_section, Text(contains='назад', ignore_case=True), state=SettingStates.change_number)


    dp.register_message_handler(echo, state = '*')