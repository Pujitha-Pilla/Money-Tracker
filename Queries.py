import sqlite3
from sqlite3 import Error

def create_connection(db_path):
	conn = None
	try:
		conn = sqlite3.connect(db_path,check_same_thread=False)
		conn.row_factory = sqlite3.Row
		#c = conn.cursor()
		return conn
	except Error as e:
		print (e)
	return conn

def sql_select_query(conn, query, var):
	cur = conn.cursor()
	cur.execute(query,var)
	rows = cur.fetchall()
	return rows

def sql_insert_query(conn, query, var):
	cur = conn.cursor()
	cur.execute(query,var)
	conn.commit()
