import mysql.connector
from datetime import datetime, timedelta


class SQLighter:

	def __init__(self):
		"""Подключаемся к БД"""
		# self.user_id = user_id
		self.adv_mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='1916Nikita565.',
			database='testdb',
			)
		self.adv_cursor = self.adv_mydb.cursor(buffered=True)
		self.user_mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='1916Nikita565.',
			database='users',
			)
		self.user_cursor = self.user_mydb.cursor(buffered=True)
		self.hash_mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='1916Nikita565.',
			database='hash',
			)
		self.hash_cursor = self.hash_mydb.cursor(buffered=True)
		self.countriessub_mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='1916Nikita565.',
			database='countries_subscribers',
			)
		self.countriessub_cursor = self.countriessub_mydb.cursor(buffered=True)
		self.temporaryparams_mydb = mysql.connector.connect(
			host='localhost',
			user='root',
			passwd='1916Nikita565.',
			database='temporary_params',
			)
		self.temporaryparams_cursor = self.temporaryparams_mydb.cursor(buffered=True)

# """Действия с бд юзеров"""

	def create_users_db(self):
		db = "CREATE DATABASE `{}`".format('users')
		return self.adv_cursor.execute(db)

	def create_users_table(self):
		users_table = "CREATE TABLE `{}` (`ID` INT AUTO_INCREMENT PRIMARY KEY, `user_id` VARCHAR(255), `first_name` VARCHAR(255), `last_name` VARCHAR(255), `username` VARCHAR(255), `ip` VARCHAR(255))".format('users')
		return self.user_cursor.execute(users_table)

	def add_user(self, user_id, first_name, last_name, username, ip):
		sql = "INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `username`, `ip`) VALUES (%s,%s,%s,%s,%s)"
		val = user_id, first_name, last_name, username, ip
		self.user_cursor.execute(sql, val)
		self.user_mydb.commit()
		self.user_mydb.close()

	def check_user(self, user_id):
		sql = "SELECT * FROM users WHERE user_id = {0}".format(user_id)
		self.user_cursor.execute(sql)
		data = self.user_cursor.fetchone()
		return data

	def get_users_data(self):
		sql = "SELECT * FROM users"
		self.user_cursor.execute(sql)
		return self.user_cursor.fetchall()


	def clear_users_table(self, user_id):
		sql = "TRUNCATE TABLE `{}`".format(user_id)
		self.user_cursor.execute(sql)

	# def get_bolhasi_status(self, user_id):
	# 	sql = "SELECT bolhasistatus FROM users WHERE user_id = {0}".format(user_id)
	# 	self.user_cursor.execute(sql)
	# 	data = self.user_cursor.fetchone()
	# 	print(bool(data[0]))
	# 	return bool(data[0])



# """Действия с основной бд"""

	def create_advertisement_table(self, user_id):
		db_table = "CREATE TABLE `{}` (`Площадка` VARCHAR(255), `Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)".format(user_id)
		return self.adv_cursor.execute(db_table)


	def add_advertisement(self, user_id, platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		sql = "INSERT INTO `{}` (`Площадка`, `Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(user_id)
		val = platform, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
		self.adv_cursor.execute(sql, val)
		self.adv_mydb.commit()


	def get_advertisement_data(self, user_id):
	# """Получаем все элементы бд"""
		sql = "SELECT * FROM `{}`".format(user_id)
		self.adv_cursor.execute(sql)
		return self.adv_cursor.fetchall()

	def len_advertisement_data(self, user_id):
	# """Получаем длину ВРЕМЕННОЙ бд"""
		sql = "SELECT * FROM `{}`".format(user_id)
		self.adv_cursor.execute(sql)
		length = len(self.adv_cursor.fetchall())
		return length


	def check_advestisement(self, user_id, adv_url):
		sql = "SELECT * FROM `{}` WHERE `Ссылка на объявление`=`%s`".format(user_id)
		adr = (adv_url, )
		self.adv_cursor.execute(sql, adr)
		data = self.adv_cursor.fetchone()
		return data

	def clear_advestisement(self, user_id):
		sql = "TRUNCATE TABLE `{}`".format(user_id)
		return self.adv_cursor.execute(sql)


# """Действия с временной бд"""

	def create_hash_table(self, tb_name):
		hash_table = "CREATE TABLE `{}` (`Название объявления` VARCHAR(255), `Цена объявления` VARCHAR(255), `Дата создания объявления` VARCHAR(255), `Ссылка на объявление` VARCHAR(255), `Местоположение` VARCHAR(255), `Ссылка на изображение` VARCHAR(255), `Имя продавца` VARCHAR(255), `Номер продавца` VARCHAR(255), `Количество объявлений продавца` VARCHAR(255), `Дата регистрации` VARCHAR(255) DEFAULT NULL, `Бизнесс аккаунт` VARCHAR(255) DEFAULT NULL)".format(tb_name)
		return self.hash_cursor.execute(hash_table)


	def add_hash_advertisement(self, user_id, adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business):
		sql = "INSERT INTO `{}` (`Название объявления`, `Цена объявления`, `Дата создания объявления`, `Ссылка на объявление`, `Местоположение`, `Ссылка на изображение`, `Имя продавца`, `Номер продавца`, `Количество объявлений продавца`, `Дата регистрации`, `Бизнесс аккаунт`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(user_id)
		val = adv_name, adv_price, adv_reg, adv_url, location, adv_image_url, seller_name, seller_tel_number, seller_count_adv, seller_reg_data, check_business
		self.hash_cursor.execute(sql, val)
		return self.hash_mydb.commit()


	def get_hash_data(self, user_id):
	# """Получаем все элементы ВРЕМЕННОЙ бд"""
		sql = "SELECT * FROM `{}`".format(user_id)
		self.hash_cursor.execute(sql)
		return self.hash_cursor.fetchall()
		self.hash_mydb.close()

	def clear_hash_data(self, tb_name):
		sql = "TRUNCATE TABLE `{}`".format(tb_name)
		return self.hash_cursor.execute(sql)


	def len_hash_data(self, user_id):
	# """Получаем длину ВРЕМЕННОЙ бд"""
		sql = "SELECT * FROM `{}`".format(user_id)
		self.hash_cursor.execute(sql)
		length = len(self.hash_cursor.fetchall())
		return length


	# def delete_database(self):
	# 	db = "DROP DATABASE `users_id`"
	# 	return self.user_cursor.execute(db)

	def delete_table(self, tb_name):
		sql = "DROP TABLE `{}`".format(tb_name)
		return self.adv_cursor.execute(sql)

	def delete_hash_table(self, tb_name):
		sql = "DROP TABLE `{}`".format(tb_name)
		return self.hash_cursor.execute(sql)

	def delete_temporary_params_table(self, tb_name):
		sql = "DROP TABLE `{}`".format(tb_name)
		return self.temporaryparams_cursor.execute(sql)

	def delete_users_table(self, tb_name):
		sql = "DROP TABLE `{}`".format(tb_name)
		return self.user_cursor.execute(sql)

	def delete_users_subsc_database(self, country):
		sql = "DROP DATABASE `{}`".format(country)
		return self.adv_cursor.execute(sql)	


	# def update_subsc(self, bolhasistatus, user_id):
	# 	sql = "UPDATE users SET bolhasistatus = %s WHERE user_id = %s"
	# 	val = (bolhasistatus, user_id)
	# 	self.user_cursor.execute(sql, val)
	# 	self.user_mydb.commit()


# bolhasi
	def create_countries_sub(self):
		db = "CREATE DATABASE `{}`".format('countries_subscribers')
		return self.adv_cursor.execute(db)

	def create_countries_sub_table(self, country):
		countrysub_table = "CREATE TABLE `{}` (`ID` INT AUTO_INCREMENT PRIMARY KEY, `user_id` VARCHAR(255), `time_until` VARCHAR(255))".format(country)
		return self.countriessub_cursor.execute(countrysub_table)

	def add_subscriber(self, country, user_id, time_until = datetime.now()):
		sql = "INSERT INTO `{}` (`user_id`, `time_until`) VALUES (%s,%s)".format(country)
		val = user_id, time_until
		self.countriessub_cursor.execute(sql, val)
		return self.countriessub_mydb.commit()
		# self.countriessub_mydb.close()

	def check_subscriber(self, country, user_id):
		sql = "SELECT * FROM `{0}` WHERE user_id = {1}".format(country, user_id)
		self.countriessub_cursor.execute(sql)
		data = self.countriessub_cursor.fetchone()
		return data

	def get_subscriber_time(self, country, user_id):
		sql = "SELECT time_until FROM `{0}` WHERE user_id = {1}".format(country, user_id)
		self.countriessub_cursor.execute(sql)
		sub_time = self.countriessub_cursor.fetchone()
		a = sub_time[0]
		b = a.split("-")
		c = b[2].split(" ")
		d = c[1].split(":")
		k = d[2].split(".")
		return datetime(int(b[0]), int(b[1]), int(c[0]), int(d[0]), int(d[1]), int(k[0]), int(k[1]))


	def update_subsc_time(self, user_id, time_until, country):
		sql = "UPDATE `{}` SET time_until = %s WHERE user_id = %s".format(country)
		val = (time_until, user_id)
		self.countriessub_cursor.execute(sql, val)
		self.countriessub_mydb.commit()


	def clear_sub_data(self, country):
		sql = "TRUNCATE TABLE `{}`".format(country)
		return self.countriessub_cursor.execute(sql)

# Временные параметры
	def create_temporary_params(self):
		db = "CREATE DATABASE `{}`".format('temporary_params')
		return self.adv_cursor.execute(db)


	def create_temporary_params_table(self, user_id):
		params_table = "CREATE TABLE `{}` (`country` VARCHAR(255), `link` VARCHAR(255), `adv_count` VARCHAR(255), `seller_adv` VARCHAR(255), `adv_reg_data` VARCHAR(255), `reg_seller_data` VARCHAR(255), `business` VARCHAR(255))".format(user_id)
		return self.temporaryparams_cursor.execute(params_table)

	def add_temporary_params(self, user_id, country, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business):
		sql = "INSERT INTO `{}` (`country`, `link`, `adv_count`, `seller_adv`, `adv_reg_data`, `reg_seller_data`, `business`) VALUES (%s,%s,%s,%s,%s,%s,%s)".format(user_id)
		val = country, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business
		self.temporaryparams_cursor.execute(sql, val)
		self.temporaryparams_mydb.commit()

	def get_temporary_params(self, user_id):
	# """Получаем все элементы ВРЕМЕННОЙ бд"""
		sql = "SELECT * FROM `{}`".format(user_id)
		self.temporaryparams_cursor.execute(sql)
		all_data = self.temporaryparams_cursor.fetchone()
		return all_data


	def get_temp_country(self, user_id):
		sql = "SELECT country FROM `{}`".format(user_id)
		self.temporaryparams_cursor.execute(sql)
		temp_country = self.temporaryparams_cursor.fetchone()[0]
		return temp_country


	def clear_temporary_params_table(self, user_id):
		sql = "TRUNCATE TABLE `{}`".format(user_id)
		return self.temporaryparams_cursor.execute(sql)


#  user_id, link, adv_count, seller_adv, adv_reg_data, reg_seller_data, business
	# def get_users_data(self):
	# 	sql = "SELECT * FROM users"
	# 	self.user_cursor.execute(sql)
	# 	return self.user_cursor.fetchall()

	# def check_advestisement(self, user_id, adv_url):
	# 	sql = "SELECT * FROM `{}` WHERE adv_url = {}".format(user_id, adv_url)
	# 	self.adv_cursor.execute(sql)
	# 	self.adv_cursor.fetchone()


# sql = "SELECT * FROM users WHERE user_id = {0}".format(user_id)
# 		self.user_cursor.execute(sql)
# 		data = self.user_cursor.fetchone()
# 		return data

		# def check_subscriber(self, user_id):
		# 	sql = "SELECT * FROM `2029023685` WHERE user_id = {0}".format(user_id)
		# 	self.user_cursor.execute(sql)
		# 	data = self.user_cursor.fetchone()
		# 	return data

	# def show_databases(self):
	# 	self.cursor.execute('SHOW DATABASES')
	# 	for i in self.cursor:
	# 		if i == ('testdb',):
	# 			print('testdb',i)
	# 		else:
	# 			db = "DROP DATABASE `{}`".format(i)
	# 			self.cursor.execute(db)

	# delete


	# def delete_table(self, user_id):
	# 	duba = "DROP TABLE `{}`".format(user_id)
	# 	return self.adv_cursor.execute(duba)

	# def update_url(self, used_urls, user_id):
	# 	with self.connection:
	# 		return self.cursor.execute("INSERT INTO `subscriber` (`user_id`, `used_urls`) VALUES (?,?)", (user_id, used_urls,))
		# return self.cursor.execute("UPDATE 'subscriber' SET `used_urls` = ? WHERE `user_id` = ?", (user_id, used_urls))


	# def close(self):
	# 	self.connection.close()


if __name__ == '__main__':
	sq = SQLighter()
	sq.clear_sub_data("bazar.lu")
	# sq.create_countries_sub()
	# sq.add_subscriber("bazar.lu", 2029023685)
	# sq.create_countries_sub_table("bolha.si")
	# sq.create_countries_sub_table("bazar.lu")
	# sq.delete_users_subsc_database('countries_subscribers')
	# sq.create_countries_sub_table("bazar.lu")
	# sq.delete_users_table('users')
	# sq.create_users_table()
	# sq.clear_hash_data(2029023685)
	# sq.clear_advestisement(2029023685)
	# sq.add_temporary_params(2029023685, "bolha.si", 'https://www.bolha.com/index.php?ctl=search_ads&keywords=apple', '25', 'нет', '21.03.2015', 'нет', 'нет')
	# sq.delete_temporary_params_table(2029023685)
	# sq.clear_users_table('users')
	# sq.delete_table(2029023685)
	# sq.delete_hash_table(2029023685)
	# sq.create_advertisement_table(2029023685)
	# sq.create_hash_table(2029023685)
	# sq.delete_hash_table(1917134377)
	# sq.delete_table(1917134377)
	# if sq.get_temp_country(2029023685) == 'bolha.si':
	# 	print('kakish')
	# sq.create_temporary_params_table(2029023685)
	# a = sq.get_subscriber_time('bolhasi', 2029023685) - datetime.now()
	# print(a)
