# https://surik00.gitbooks.io/aiogram-lessons/content/chapter5.html
# ! https://www.youtube.com/watch?v=wj1Vwq3IrL4&list=PLwVBSkoL97Q3phZRyInbM4lShvS1cBl-U

# https://botfather.dev/blog/kak-zajti-v-razrabotku-botov-1
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton
from callback_data import *
from aiogram import types

# Одна кнопка
btnHello = KeyboardButton("Start 👋")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnHello)

# Много кнопок
#button1 = KeyboardButton("🔔")
InfoP = KeyboardButton("Персонаж")
Stat = KeyboardButton("Статистика")
Items = KeyboardButton("Инвентарь")
Locations = KeyboardButton("Карта")
Par_O = KeyboardButton("Общая")
Par_pers = KeyboardButton("Обо мне")
Back_menu = KeyboardButton("Назад в меню") # Or KeyboardButton("/menu")
Meditation = KeyboardButton("Медитация")

Menu1 = ReplyKeyboardMarkup(resize_keyboard=True).row(Back_menu)
menuO = ReplyKeyboardMarkup(resize_keyboard=True).row(InfoP, Stat, Locations)
Pers00 = ReplyKeyboardMarkup(resize_keyboard=True).row(Back_menu, Items, Meditation)
Stat00 = ReplyKeyboardMarkup(resize_keyboard=True).row(Back_menu, Par_pers, Par_O)

# m_kb2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(Pers00)

# дополнительное добавление кнопок
inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)


# Кнопки отправки контакта и геолокации
inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_kb_full.add(inline_btn_3, inline_btn_3, inline_btn_3)
inline_kb_full.row(inline_btn_3, inline_btn_3, inline_btn_3)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))

# Choice

choice = InlineKeyboardMarkup(row_width=2, inline_keyboard= 
	[
		[InlineKeyboardButton(text = 'Buy pear', callback_data=buy_callback.new(item_name='pear', quantity = 1)), #, quantity=1)),
		 InlineKeyboardButton(text = 'Buy apple', callback_data='buy:apple:5')	], 
		[InlineKeyboardButton(text = 'Отмена', callback_data='cancel')],
	])

pear_keyboard = InlineKeyboardMarkup()
pear_link = InlineKeyboardButton(text='Купи тут', url='https://ya.com')

pear_keyboard.insert(pear_link)

#--------------------------------------------------------
# For numbers

number01 = [
	types.InlineKeyboardButton(text="-10", callback_data="num_mdes"),
    types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
    types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
    types.InlineKeyboardButton(text="+10", callback_data="num_pdes"),
    types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
]
# Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
# уйдёт на следующую строку
keyboard_numb = types.InlineKeyboardMarkup(row_width=4)
keyboard_numb.add(*number01)

#----------------------------------------------------------
key_har = [
	types.InlineKeyboardButton(text="+1", callback_data="har_pn01"),
    types.InlineKeyboardButton(text="+1", callback_data="har_pn02"),
    types.InlineKeyboardButton(text="+1", callback_data="har_pn03"),
    types.InlineKeyboardButton(text="+1", callback_data="har_pn04"),
    # types.InlineKeyboardButton(text="-1", callback_data="har_mn01"),
    # types.InlineKeyboardButton(text="-1", callback_data="har_mn02"),
    # types.InlineKeyboardButton(text="-1", callback_data="har_mn03"),
    # types.InlineKeyboardButton(text="-1", callback_data="har_mn04"),
    types.InlineKeyboardButton(text="Сбросить", callback_data="har_sbros"),
    types.InlineKeyboardButton(text="Подтвердить", callback_data="har_fin")
]
# Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
# уйдёт на следующую строку
keyboard_har = types.InlineKeyboardMarkup(row_width=4)
keyboard_har.add(*key_har)

key_hero = [
	types.InlineKeyboardButton(text="Контроль", callback_data="hero_001"),
    types.InlineKeyboardButton(text="Атака", callback_data="hero_002"),
    types.InlineKeyboardButton(text="Защита", callback_data="hero_003"),
    types.InlineKeyboardButton(text="Поддержка", callback_data="hero_004"),
    types.InlineKeyboardButton(text="Ловкость", callback_data="hero_005"),
    types.InlineKeyboardButton(text="Питание", callback_data="hero_006"),
    types.InlineKeyboardButton(text="Я выбрал", callback_data="hero_000")
]
kb_hero = types.InlineKeyboardMarkup(row_width=2)
kb_hero.add(*key_hero)

# inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
# inline_kb_full.add(inline_btn_3, inline_btn_3, inline_btn_3)

kb_del = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text="Да, удалить", callback_data="del_del"))
