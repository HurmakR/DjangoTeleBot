from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tutorial.wsgi import *


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


