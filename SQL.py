import sqlite3
from sqlite3 import Error

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return conn

def create_table(conn,create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
def create_object(path):
	conn = create_connection(path)
	c = conn.cursor()
	return c
def main():

	sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
								uname text NOT NULL, password text NOT NULL, balance double precision not null default 0);"""

	sql_create_transactions_table = """CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	 									user_id integer NOT NULL, reason type text NOT NULL,
	 									type text NOT NULL,amount double precision NOT NULL,
										timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP);"""

	conn = create_connection("app_database.db")

	if conn is not None:
		create_table(conn, sql_create_users_table)
		create_table(conn, sql_create_transactions_table)
	else:
		print("Error! Cannot create database connection")

	#conn.execute("INSERT INTO users (uname,password) VALUES ('pujitha','pujitha')")
	#conn.commit()
	print("Users")
	l=conn.execute("SELECT * from users")
	for row in l:
		print (row)
	print("transactions")
	l=conn.execute("SELECT * from transactions")
	for row in l:
		print (row)
	conn.close()


if __name__ == '__main__':
	main()