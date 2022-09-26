from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import BotDB
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
for i in BotDB.get_category():
    buttons.append([InlineKeyboardButton(i[0],callback_data=i[0])])
catMenu = InlineKeyboardMarkup(inline_keyboard =buttons)
