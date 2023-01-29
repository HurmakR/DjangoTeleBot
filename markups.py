from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import BotDB
from tutorial.wsgi import *
from logs.models import Cat, Model, Partprice, Parts


#---Back to main menu Button---


btnMain = KeyboardButton('🔙 Повернутись в головне меню')

#---Main  menu---
btnRepair = KeyboardButton('⚙ Статус ремонту ⚙')
btnPrice = KeyboardButton('💸 Вартість ремонту 💸')
btnShipping = KeyboardButton('📦 Реквізити для відправки Новою Поштою 📦')
btnContacts = KeyboardButton('📍 Контакти, графік роботи 📍')
btnPayment = KeyboardButton('💳 Реквізити для оплати 💳')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True,row_width=1).add(btnRepair, btnPrice, btnShipping, btnContacts)
mainMenuExtended = ReplyKeyboardMarkup(resize_keyboard = True,row_width=2).add(btnRepair, btnPrice, btnShipping,
                                                                               btnContacts, btnPayment)
# Inline menu Category from the same sqlite db table
BotDB = BotDB('price.db')
buttons=[]

for i in Cat.objects.all().order_by('category'):#BotDB.get_category():
    buttons.append([InlineKeyboardButton(i.category,callback_data=i.category)])
catMenu = InlineKeyboardMarkup(inline_keyboard =buttons)

