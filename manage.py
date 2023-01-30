#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from RemAPI import get_repair_by_id
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import markups as nav
from datetime import datetime
from logs.models import Model, Partprice, Cat

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

"""Here comes bot's handlers section. 
(it will be transferred to separate individual module later.)  
"""
storage = MemoryStorage()
load_dotenv()
bot = Bot(token=os.getenv('TELE_TOKEN'))
dp = Dispatcher(bot, storage=storage)


class RepairStatus(StatesGroup):
    waiting_for_repair_id = State()
    waiting_for_phone_number = State()


class PriceStatus(StatesGroup):
    waiting_for_model = State()
    waiting_for_price = State()


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    """ Handler for starting command"""
    if message.from_user.id == 419685899 or 705036271:  #hardcoded useres id to output special Bot menu items
        await bot.send_message(message.from_user.id, "Вітаємо, {0.first_name}!\nЦей бот допоможе Вам "
                                                     "отримати інформацію про стан ремонту, ціни на послуги та іншу корисну інформацію .".format(
            message.from_user), reply_markup=nav.mainMenuExtended)
    else: #regular menu for all other users
        await bot.send_message(message.from_user.id, "Вітаємо, {0.first_name}!\nЦей бот допоможе Вам "
                     "отримати інформацію про стан ремонту, ціни на послуги та іншу корисну інформацію .".format(
                         message.from_user), reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    """ processing input from keyboard"""
    if message.text == '⚙ Статус ремонту ⚙':# starting stages from RepairStatus class
        await bot.send_message(message.from_user.id, 'Введіть номер квитанції (<i>тільки цифри <s>ВО</s><b>123456</b></i>)', parse_mode='html')
        await RepairStatus.waiting_for_repair_id.set()
    elif message.text == '💸 Вартість ремонту 💸':# starting stages from PriceStatus class,
        # forms inline keys filled from model Cat
        buttons = []
        for i in Cat.objects.all().order_by('category'):
            buttons.append([InlineKeyboardButton(i.category, callback_data=i.category)])
        catMenu = InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(message.chat.id, '💻📱 Оберіть категорію: ⌚🖥', reply_markup=catMenu)
        await PriceStatus.waiting_for_model.set()
    elif message.text == '📦 Реквізити для відправки Новою Поштою 📦':#text message output
        await bot.send_message(message.chat.id, '<b>Реквізити для адресної відправки: </b>\n\n'
                                                '<i>м. Львів, вул. К. Левицького 6, </i>\n'
                                                '<i>0673233095,отримувач: Гурмак Роман Дмитрович.</i> \n'
                                                'Пересилка здійснюється за Ваш рахунок. \n\n'
                                                'Вкладіть будь ласка детальний опис несправності та'
                                                ' контактну інформацію з email включно.\n\n'
                                                '🍏 Для Watch, Airpods вкажіть в описі, з яким iOs-пристроєм'
                                                ' працюють в парі та версію iOs на ньому.\n'
                                                '🍎 Для Mac, iPhone, iPad, Watch обов\'язково '
                                                'вимкніть локатор.\n\n'
                                                '❗️<b>У зв\'язку з дією положення про військовий стан, термін ремонту'
                                                ' може становити до 120 діб.</b>\n'
                                                '❗️<b>Сервісний центр не несе відповільності за збереження інформації,'
                                                ' будь ласка перед відправленням збережіть резервну копію,'
                                                ' якщо це можливо.</b>\n'
                                                '❗️<b>Нанесене захисне скло чи плівка можуть бути демонтовані,'
                                                ' їхня цілісність та повернення не гарантуються.</b> '
                                                , parse_mode='html')
    elif message.text == '📍 Контакти, графік роботи 📍':#text message output
        await bot.send_message(message.chat.id, '<b>Наша адреса: </b>\n\n'
                                                '<i>м. Львів, вул. К. Левицького 6, </i>\n'
                                                '<i>0800-330-434, 067-323-30-95.</i> \n'
                                                '<i>www.rosan-service.com.ua </i>\n\n'
                                                '<b>Графік роботи: </b>\n\n'
                                                '<i>Понеділок-пятницю з 10:00 до 19:00 </i>\n'
                                                '<i>Субота з 11:00 до 16:00.</i> \n'
                                                '<i>Неділя - вихідний </i>\n\n', parse_mode='html')
    elif message.text == '💳 Реквізити для оплати 💳':#text message output
        await bot.send_message(message.chat.id, '<b>Одержувач платежу: </b>\n\n'
                                                '<b>Найменування одержувача:   ФОП Гурмак Роман Дмитрович </b>\n'
                                                '<b>Код одержувача:                            2899103773</b> \n'
                                                '<b>Назва банку:                       АТ КБ «ПриватБанк» </b>\n'
                                                '<b>Рахунок одержувача у форматі IBAN:</b> \n'
                                                '<b>UA983052990000026005011013493</b>\n\n'
                                                '<b>Призначення платежу: Оплата за ремонт ХХХХХХ</b>\n'
                                                '<b>Сума до оплати: </b>'

                                                , parse_mode='html')

    else:#wrong text entered reply message
        await message.reply('Скористайтесь меню або введіть команду /start')


@dp.callback_query_handler(lambda call: True, state=PriceStatus.waiting_for_model)
async def price_model(callback_query: types.CallbackQuery, state: FSMContext):
    """Handler shows devices models  filtered by chosen earlier model category  """
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_reply_markup()
    buttons = []
    async for models_filtered in Model.objects.filter(modelcat=callback_query.data).order_by('modelname'):
        buttons.append([InlineKeyboardButton(str(models_filtered), callback_data=str(models_filtered))])
    modMenu = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    await bot.send_message(callback_query.from_user.id, f'Оберіть модель {callback_query.data}:', reply_markup=modMenu)
    await PriceStatus.waiting_for_price.set()


@dp.callback_query_handler(lambda call: True, state=PriceStatus.waiting_for_price)
async def price_result(callback_query: types.CallbackQuery, state: FSMContext):
    """Handler shows messages with prices for chosen device model  """
    #BotDB.add_log(callback_query.from_user.first_name, callback_query.from_user.last_name, callback_query.from_user.username,
                  #callback_query.data, datetime.now())
    await callback_query.message.edit_reply_markup()
    await bot.send_message(callback_query.from_user.id, f'{callback_query.data}:')
    price_out = ''
    async for mod in Partprice.objects.filter(idmodel__modelname=callback_query.data):
        price_out += f'{mod.idpart.partname}:\n' \
                     f'Обмінна ціна {mod.pricepart or "*"} | Сток ціна {mod.pricestock or "*"} грн. \n'
    await bot.send_message(callback_query.from_user.id, price_out)
    await state.finish()


@dp.message_handler(state=RepairStatus.waiting_for_repair_id)
async def enter_repair_id(message : types.Message, state: FSMContext):
    """Handler searches for entered by the user repair id  """
    #BotDB.add_log(message.from_user.first_name, message.from_user.last_name,
    #              message.from_user.username,
    #              message.text, datetime.now())
    try:
        global data
        async with state.proxy() as data:
            data = get_repair_by_id(message.text)['data'][0]
        await bot.send_message(message.chat.id, '✅ Ремонт знайдено ✅\nВкажіть останні 4 цифри номеру телефона, зареєстрованого в ремонті')
        await RepairStatus.waiting_for_phone_number.set()
    except:
        await bot.send_message(message.chat.id, '❌ Ремонту з таким номером не знайдено ❌\nВведіть коректний номер квитанції')
        await state.finish()

@dp.message_handler(state=RepairStatus.waiting_for_phone_number)
async def enter_phone_number(message : types.Message, state: FSMContext):
    """Handler validates successfully found repair by entered last 4 digits from repair phone number  """
    phone_matched = False
    for phone in data['client']['phone']:
        if message.text == phone[-4::]:
            phone_matched = True
    if phone_matched:
        await bot.send_message(message.chat.id, f"<b>Пристрій: </b><i>{data['model']}</i>\n"
                                                f"<b>Серійний номер: </b><i>{data['serial']}</i>\n"
                                                f"<b>Стан ремонту: </b><i>{data['status']['name']}</i>", parse_mode='html')
    else:
        await bot.send_message(message.chat.id, '❌ Введені цифри не відповідають 4 останнім зареєстрованого номеру телефона ❌', parse_mode='html')
    await state.finish()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutorial.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':

    main()
    executor.start_polling(dp, skip_updates=True)
