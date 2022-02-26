import sqlite3
from ast import literal_eval

def sql_start():
	conn = sqlite3.connect('db.db')
	curs = conn.cursor()

	# создание таблицы Base_Persons в БД

#		                
	curs.execute('''CREATE TABLE IF NOT EXISTS Base_characters(
	                Id INTEGER PRIMARY KEY AUTOINCREMENT,
	                Type INTEGER NOT NULL,
	                Attack INTEGER NOT NULL,
	                Defense INTEGER NOT NULL,
	                Speed INTEGER NOT NULL,
	                Control INTEGER NOT NULL,
	                HP INTEGER NOT NULL,
	                Exp INTEGER NOT NULL,
	                Duh_S INTEGER NOT NULL,
	                Ment_S INTEGER NOT NULL
	            );''')

	# заполнение таблицы Base_Persons записями из файла
	try:
		#  open('f1').read().decode('utf8')
		with open('base.txt', encoding="utf-8") as f:
			for rec in f:
				r = literal_eval(rec)
				try:
					curs.execute('''INSERT INTO Base_characters
						VALUES(?,?,?,?,?,?,?,?,?,?);''',r)
				except sqlite3.IntegrityError as err:
					print(err, r[0], '- Insertion ignore...')
					continue
	except IOError as err:
		print(err)
	# Таблица пользователей
	curs.execute('''CREATE TABLE IF NOT EXISTS Base_Users(
	                Id INTEGER PRIMARY KEY,
	                User_id INTEGER NOT NULL,
	                Number_person INTEGER NOT NULL,
	                Type INTEGER NOT NULL,
	                Attack INTEGER NOT NULL,
	                Defense INTEGER NOT NULL,
	                Speed INTEGER NOT NULL,
	                Control INTEGER NOT NULL,
	                HP INTEGER NOT NULL,
	                Exp INTEGER NOT NULL,
	                Duh_S INTEGER NOT NULL,
	                Ment_S INTEGER NOT NULL
	            );''')		

	conn.commit()

	# выборка содержимого таблицы Base_characters из БД
	ss = curs.execute("SELECT * FROM Base_characters;").fetchall()
	count1 = curs.execute("SELECT COUNT(Type) FROM Base_characters;").fetchall()[0][0] # [0][0] достает число из запроса

	print('№, User_Id, № перса, Тип, атака, защита, скорость, контроль, жизнь, Опыт, Дух.сила, Мент.сила)')
	for s in ss:
		print(s)
	print('\n Кол-во персонажей:', count1)

	conn.close()

def sql_info(func):
	conn = sqlite3.connect('db.db')
	curs = conn.cursor()
	def wrapper(*args):
		return func(*args)
	conn.close()
	return wrapper
#sql_start()

def info_hero(numb):
	conn = sqlite3.connect('db.db')
	curs = conn.cursor()
	m11 = curs.execute("SELECT * FROM Base_characters WHERE Id = ?;", tuple([numb])).fetchall()[0]
	conn.close()
	return list(m11)

def pers_hero_id(id):
	conn = sqlite3.connect('db.db')
	curs = conn.cursor()
	m12 = curs.execute("SELECT * FROM Base_Users WHERE User_id = ?;", tuple([id])).fetchall()[0]
	conn.close()
	return list(m12)
	
