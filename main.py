# One-bot

from config import TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import keyboards as kb
from callback_data import *
from setting_commands import *
from datetime import datetime, date, time

from  db import *
import sqlite3

sql_start()

# conn = sqlite3.connect('db.db')
# curs = conn.cursor()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def set_all_default_commands(bot: Bot):
    print('Commands started')
    await set_default_commands(bot)
# Commands, https://botfather.dev/dashboard

print('Бот @one4bot запущен')

@dp.message_handler(commands=['start'])
# @sql_info # декоратор на включение/отключение от бд
async def process_start(message: types.Message):
    conn = sqlite3.connect('db.db')
    curs = conn.cursor()
    id = message.chat.id
    m = curs.execute("SELECT User_id FROM Base_Users WHERE User_id = ?;", tuple([id])).fetchall() 

    if m != []:
        if id == m[0][0]:
            print(m[0][0], '-->',id)
            text = f'Привет, {message.chat.first_name}!\n\n' + 'Для удаления героя нажмите /delete'
            print(datetime.now())
    else:
        print('m[0] пуст')
        text = 'Привет, дорогой гость, выбери себе персонажа нажав /hero'
    conn.close()
    await bot.send_message(message.from_user.id, text, reply_markup=kb.Menu1)

@dp.message_handler(commands=['menu'])
async def process_menu(message: types.Message):
	await bot.send_message(message.from_user.id, 'Menu', reply_markup=kb.menuO)

@dp.message_handler(commands=['stat'])
async def process_stat(message: types.Message): 
	await bot.send_message(message.from_user.id, 'Статистика', reply_markup=kb.Stat00)


# Text
@dp.message_handler(text = 'Статистика')
async def process_reply(message: types.Message):
	await bot.send_message(message.from_user.id, f'Ваша статистика 💳\nТвой континент {message.chat.id}\n\n\nРаздел в разработке', reply_markup=kb.Stat00)

@dp.message_handler(text = 'Персонаж')
async def process_reply(message: types.Message):
    har = pers_hero_id(message.chat.id)
    text = f'Класс: {har[3]}\nСила: {har[4]}\nЗащита: {har[5]}\nВыносливость: {har[6]}\nКонтроль: {har[7]}\n\
    Жизнь: {har[8]}\nОпыт: {har[9]}\nДух.сила: {har[10]}\nМент.Сила: {har[11]}'
    await bot.send_message(message.from_user.id, text, reply_markup=kb.Pers00)

@dp.message_handler(text = 'Назад в меню')
async def process_reply(message: types.Message):
	await bot.send_message(message.from_user.id, 'Меню', reply_markup=kb.menuO)

@dp.message_handler(text = 'Обо мне')
async def process_reply(message: types.Message):
    await message.reply('В разработке')

@dp.message_handler(text = 'Общая')
async def process_reply(message: types.Message):
    await message.reply('В разработке')

@dp.message_handler(text = 'Карта')
async def process_reply(message: types.Message):
    await message.reply('В разработке')

@dp.message_handler(text = 'Медитация')
async def process_reply(message: types.Message):
    await message.reply('В разработке')
#--------------------
@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
	await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb_full)

# Inline button 6.02

@dp.message_handler(commands=['items'])
async def process_command_1(message: types.Message):
	await message.answer(text = 'Покупка', reply_markup=kb.choice)

@dp.callback_query_handler(buy_callback.filter(item_name='pear'))
async def buying_pear(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=60)
	logging.info(f'callback_data = {call.data}')
	logging.info(f'callback_data dict = {callback_data}')
	print(f'callback_data = {call.data}', type(call.data))
	print(f'callback_data dict = {callback_data}')
	quantity = callback_data.get('quantity')
	await call.message.answer(f'Вы выбрали груши. Всего: {quantity}. Спасибо.', reply_markup=kb.pear_keyboard)

@dp.callback_query_handler(buy_callback.filter(item_name='apple'))
async def buying_apple(call: types.CallbackQuery, callback_data: dict):
	await call.answer(cache_time=60)
	logging.info(f'callback_data = {call.data}')
	logging.info(f'callback_data dict = {callback_data}')
	print(f'callback_data = {call.data}', type(call.data))
	print(f'callback_data dict = {callback_data}')
	quantity = callback_data.get('quantity')
	await call.message.answer(f'Вы выбрали яблоки. Всего: {quantity}. Спасибо.', reply_markup=kb.pear_keyboard)

#callback_query.data[-1]
@dp.callback_query_handler(text = 'cancel')
async def cancel(call: types.CallbackQuery):
	await call.answer('You cancel', show_alert=True)
	await call.message.edit_reply_markup()

#------------------------------------------------------------
# Числа
#------------------------------------------------------------
user_data = {}
#haracters = str(call.from_user.id)+'_har'
user_data['haracters_base'] = {'0': 0, '1':0, '2':0, '3':0}

async def update_num_text(message: types.Message, new_value: int):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Укажите число: {new_value}", reply_markup=kb.keyboard_numb)

@dp.message_handler(commands='numbers')
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    print(message.from_user.id, message.from_user.first_name) # id пользователя
    print(message.from_user)
    print(user_data, '\n')
    await message.answer(f"Добрый день {message.from_user.first_name} \nУкажите число: 0", reply_markup=kb.keyboard_numb)

@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: types.CallbackQuery):
    # Получаем текущее значение для пользователя, либо считаем его равным 0
    user_value = user_data.get(call.from_user.id, 0)
    # Парсим строку и извлекаем действие, например `num_incr` -> `incr`
    action = call.data.split("_")[1]
    if action == "incr":
        user_data[call.from_user.id] += 1
        await update_num_text(call.message, user_data[call.from_user.id])
    elif action == "decr":
        user_data[call.from_user.id] -= 1
        await update_num_text(call.message, user_data[call.from_user.id])
    elif action == "mdes":
        user_data[call.from_user.id] -= 10
        await update_num_text(call.message, user_data[call.from_user.id])
    elif action == "pdes":
        user_data[call.from_user.id] += 10
        await update_num_text(call.message, user_data[call.from_user.id])
    elif action == "finish":

        # Если бы мы не меняли сообщение, то можно было бы просто удалить клавиатуру
        # вызовом await call.message.delete_reply_markup().
        # Но т.к. мы редактируем сообщение и не отправляем новую клавиатуру, 
        # то она будет удалена и так.

        await call.message.edit_text(f"Итого: {user_value}")
    # Не забываем отчитаться о получении колбэка
    await call.answer()

#------------------------------------------------------------
# Инлайн с характеристиками
#------------------------------------------------------------
async def update_har_text(message: types.Message, n_value: dict):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Характеристики:\n \
        Сила: {n_value['0']}\n \
        Защита: {n_value['1']}\n \
        Выносливость: {n_value['2']}\n \
        Контроль: {n_value['3']}", reply_markup=kb.keyboard_har)

@dp.message_handler(commands='har')
async def cmd_har(message: types.Message):
    # haracters = str(message.from_user.id)+'_har' # key
    # user_data[haracters] = user_data.get(haracters, {'0': 0, '1':0, '2':0, '3':0})
    # print(haracters, user_data[haracters])
    await message.answer("Давай распределим характеристики.\nПорядок кнопок:\nсила, ловкость, имуннитет, интеллект", reply_markup=kb.keyboard_har)

@dp.callback_query_handler(Text(startswith="har_"))
async def callbacks_num(call: types.CallbackQuery):
    haracters = str(call.from_user.id) + '_har'
    user_data[haracters] = user_data.get(haracters, {'0': 0, '1':0, '2':0, '3':0})
    # Парсим строку и извлекаем действие, например `num_incr` -> `incr`
    action = call.data.split("_")[1]
    
    print(haracters, user_data[haracters])
    if action == "pn01":
        user_data[haracters]['0'] += 1
        await update_har_text(call.message, user_data[haracters])
    elif action == "pn02":
        user_data[haracters]['1'] += 1
        await update_har_text(call.message, user_data[haracters])
    elif action == "pn03":
        user_data[haracters]['2'] += + 1
        await update_har_text(call.message, user_data[haracters])
    elif action == "pn04":
        user_data[haracters]['3'] += 1
        await update_har_text(call.message,user_data[haracters])
    # elif action == "mn01":
    #     user_data[haracters]['0'] -= 1
    #     await update_har_text(call.message, user_data[haracters])
    # elif action == "mn02":
    #     user_data[haracters]['1'] -= 1
    #     await update_har_text(call.message, user_data[haracters])
    # elif action == "mn03":
    #     user_data[haracters]['2'] -= 1
    #     await update_har_text(call.message, user_data[haracters])
    # elif action == "mn04":
    #     user_data[haracters]['3'] -= 1
    #     await update_har_text(call.message, user_data[haracters])
    elif action == "sbros":
        user_data[haracters] = {'0': 0, '1':0, '2':0, '3':0}
        await update_har_text(call.message, user_data[haracters])
    elif action == "fin":
        await call.message.edit_text(f"Итого: {user_data[haracters]}")
    # Не забываем отчитаться о получении колбэка
    await call.answer()


#--------------------------------------------------
# Create hero
#--------------------------------------------------
hero_num = {}
@dp.message_handler(commands='hero')
async def cmd_har(message: types.Message):
    conn = sqlite3.connect('db.db')
    curs = conn.cursor()
    id = message.chat.id
    m = curs.execute("SELECT User_id FROM Base_Users WHERE User_id = ?;", tuple([id])).fetchall() 

    if m != []:
        if id == m[0][0]:
            print(m[0][0], '-->',id)
            #m = curs.execute("SELECT COUNT(Type) FROM Base_Persons;").fetchall()[0][0]
            text = 'Привет, у тебя есть герой!\n'+str('...')
            await message.answer(text)
    else:
        await message.answer("Как выберешь нажми: \"Я выбрал\"", reply_markup=kb.kb_hero)

async def update_hero_text(message: types.Message, n_ve: int):
    
    if n_ve[0] == 1 and n_ve[1] > 0:
        conn = sqlite3.connect('db.db')
        curs = conn.cursor()
        m11 = curs.execute("SELECT * FROM Base_characters WHERE Id = ?;", tuple([n_ve[1]])).fetchall()[0]
        # print(m11)
        m11 = list(m11)
        m11[0] = message.chat.id
        m11 = tuple(m11)
        curs.execute('''INSERT INTO Base_Users(User_id, Number_person, Type, Attack, 
            Defense, Speed, Control,HP, Exp, Duh_S, Ment_S) VALUES(?,1,?,?,?,?,?,?,?,?,?);''', m11).fetchall()
        conn.commit()
        conn.close()
        print('\nCreate hero')
        print(m11)
        await message.edit_text(f"Герой выбран")
    else:
        m11 = info_hero(n_ve[1])
        print('<--- Снизу message.from_user--->')
        print(message.from_user)

        v_m = ["Контроль", "Атака", "Защита", "Поддержка", "Ловкость", "Питание"][n_ve[1]-1]
        text = f'\
        Сила:           {m11[2]}\n\
      Защита:         {m11[3]}\n\
    Скорость:       {m11[4]}\n\
    Контроль:       {m11[5]}\n\
       Жизнь:          {m11[6]}'''
        await message.edit_text(f"ВЫбери героя по кнопке\nТы выбрал: {v_m}\n\n{text}", reply_markup=kb.kb_hero)

@dp.callback_query_handler(Text(startswith="hero_"))
async def callbacks_num(call: types.CallbackQuery):
    # Парсим строку и извлекаем действие, например `num_incr` -> `incr`
    hero_num[call.from_user.id] = hero_num.get(call.from_user.id, 0)
    action = call.data.split("_")[1]
    if action == "001":
        hero_num[call.from_user.id] = 1
        print(call.from_user.id)
        await update_hero_text(call.message, [0,hero_num[call.from_user.id]])
    elif action == "002":
        hero_num[call.from_user.id] = 2
        await update_hero_text(call.message, [0,hero_num[call.from_user.id]])
    elif action == "003":
        hero_num[call.from_user.id] = 3
        await update_hero_text(call.message, [0,hero_num[call.from_user.id]])
    elif action == "004":
        hero_num[call.from_user.id] = 4
        await update_hero_text(call.message, [0,hero_num[call.from_user.id]])
    elif action == "005":
        hero_num[call.from_user.id] = 5
        await update_hero_text(call.message, [0,hero_num[call.from_user.id]])
    elif action == "006":
        hero_num[call.from_user.id] = 6
        await update_hero_text(call.message,[0,hero_num[call.from_user.id]])
    elif action == "000":
        await update_hero_text(call.message, [1,hero_num[call.from_user.id]])
    # Не забываем отчитаться о получении колбэка
    await call.answer()

#--------------------------------------------------
# Delete hero
#--------------------------------------------------
hero_num = {}
@dp.message_handler(commands='delete')
async def process_stat(message: types.Message): 
    await bot.send_message(message.from_user.id, 'Удаление героя приведет к потере всего прогресса в игре. Продолжить?', reply_markup=kb.kb_del)

@dp.callback_query_handler(Text(startswith="del_"))
async def callbacks_num(call: types.CallbackQuery):
    action = call.data.split("_")[1]
    if action == "del":
        conn = sqlite3.connect('db.db')
        curs = conn.cursor()
        # print(call)
        id = call.from_user.id
        m = curs.execute('DELETE FROM Base_Users WHERE User_id = ?;', tuple([id])).fetchall() 
        conn.commit()
        conn.close()
        await bot.send_message(call.from_user.id, 'Герой удален \n\nНачать заново /start')
    # Не забываем отчитаться о получении колбэка
    await call.answer()





def hlam____mmm ():
    pass
    '''
    @dp.callback_query_handler(func=lambda c: c.data == 'button1')
    async def process_callback_button1(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')

    @dp.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
    async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
        code = callback_query.data[-1]
        if code.isdigit():
            code = int(code)
        if code == 2:
            await bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
        elif code == 5:
            await bot.answer_callback_query(
                callback_query.id,
                text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉', show_alert=True)
        else:
            await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')

    @dp.message_handler(commands=['2'])
    async def process_command_2(message: types.Message):
        await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)
    '''
    # all other

@dp.message_handler(commands=['help'])
async def process_help(message: types.Message):
      await bot.send_message(message.from_user.id, 'Нужна помощь?')

@dp.message_handler()
async def process_reply(message: types.Message):
      await message.reply('Принято!!!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)