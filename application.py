import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

import Queries as q

app = Flask(__name__)

app.config["DEBUG"] = True

db = q.create_connection("app_database.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/', methods = ['GET'])
def index():
	return render_template("index.html")


@app.route('/credit', methods = ['GET','POST'])
def credit():
	if request.method == 'POST':
		user_id = session["user_id"]
		users_balance = "SELECT balance FROM users where id = :user_id"
		rows = q.sql_select_query(db, users_balance, dict(user_id=user_id))
		balance = rows[0][0] + float(request.form.get("amount"))
		type_of_transaction = "C"
		sql_query = "INSERT INTO transactions(user_id, reason, type, amount) VALUES (:user_id, :reason,:type, :amount)"
		variable = dict(user_id=session["user_id"], reason = request.form.get("about"), type = type_of_transaction, amount = request.form.get("amount"))
		q.sql_insert_query(db, sql_query, variable)
		sql_query = "UPDATE users SET balance =:balance WHERE id =:user_id"
		variable = dict(balance = balance, user_id = user_id)
		q.sql_insert_query(db, sql_query, variable)
	return redirect("/transaction")


@app.route('/debit', methods = ['GET','POST'])
def debit():
	if request.method == 'POST':
		user_id = session["user_id"]
		amount = float(request.form.get("amount"))
		users_balance = "SELECT balance FROM users where id = :user_id"
		rows = q.sql_select_query(db, users_balance, dict(user_id=user_id))
		balance = rows[0][0]
		balance -= amount
		type = "D"
		sql_query = "INSERT INTO transactions(user_id,reason, type, amount) VALUES (:user_id,:reason,:type, :amount)"
		variable = dict(user_id=session["user_id"], reason = request.form.get("about"), type = type, amount = amount)
		q.sql_insert_query(db,sql_query, variable)
		sql_query = "UPDATE users SET balance =:balance WHERE id =:user_id"
		variable = dict(balance = balance, user_id = user_id)
		q.sql_insert_query(db, sql_query, variable)
	return redirect("/transaction")


@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form.get("username")
		pd = request.form.get("password")
		sql_query = "SELECT * from users where uname = :username"
		rows = q.sql_select_query(db,sql_query, dict(username = username))
		if(len(rows) < 1):
			flash("Username does not exists",'error')
		else:
			user_password = rows[0]["password"]
			print(user_password)
			print(generate_password_hash(pd))
			if(not check_password_hash(user_password,pd)) :
				flash("Incorrect Password",'error')
			else:
				session["user_id"] = rows[0]["id"]
				return redirect("/")
	return render_template("login.html")


@app.route('/logout',methods = ['GET','POST'])
@login_required
def logout():
	session.clear()
	return redirect("/")


@app.route('/register', methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		rows=[]
		try:
			sql_query = "SELECT uname from users where uname = :username"
			rows = q.sql_select_query(db, sql_query, username = request.form.get("username"))
			if(len(rows)>0):
				flash("User already exists")
				return render_template("register.html")
		except:
			print("rows",rows)
			pass		
		if request.form.get("password") != request.form.get("confirmPassword"):
			flash("Passwords does not match")
			return render_template("register.html")
		sql_query = "INSERT INTO users (uname,password) VALUES (:username,:password)"
		q.sql_insert_query(db, sql_query, dict(username=request.form.get("username"),password=generate_password_hash(request.form.get("password"))))
		return redirect("/")
	else:
		return render_template("register.html")

@app.route('/statement', methods = ['GET'])
@login_required
def  statement():
	sql_query = "SELECT * from transactions where user_id = :username"
	variable = dict(username = session["user_id"])
	rows = q.sql_select_query(db,sql_query,variable)
	row = q.sql_select_query(db, "SELECT balance from users where id=:id", dict(id=session["user_id"]))
	balance = row[0][0]
	return render_template("statement.html", records = rows, balance=balance)



@app.route('/transaction',methods = ['GET','POST'])
@login_required
def transaction():
	return render_template("transaction.html")


app.run()