import sqlite3
from sqlite3 import Error

def create_connection(db_path):
	conn = None
	try:
		conn = sqlite3.connect(db_path,check_same_thread=False)
		#c = conn.cursor()
		return conn
	except Error as e:
		print (e)
	return conn

def main():
	pass

if __name__ == '__main__':
	main()