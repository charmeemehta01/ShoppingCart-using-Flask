import pymysql
from app import app
from db_config import mysql
from flask import flash, session, render_template, request, redirect, url_for
		
@app.route('/add', methods=['POST'])
def add_product_to_cart():
	cursor = None
	try:
		_quantity = int(request.form['quantity'])
		_code = request.form['code']
		if _quantity and _code and request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * FROM product WHERE code=%s", _code)
			row = cursor.fetchone()
			if float(row['quantity']) >= float(_quantity) :	
				itemArray = { row['code'] : {'name' : row['name'], 'code' : row['code'], 'quantity' : _quantity, 'price' : row['price'], 'image' : row['image_url'], 'total_price': _quantity * row['price']}}
				all_total_price = 0
				all_total_quantity = 0
				session.modified = True
				if 'cart_item' in session:
					if row['code'] in session['cart_item']:
						for key, value in session['cart_item'].items():
							if row['code'] == key:
								old_quantity = session['cart_item'][key]['quantity']
								total_quantity = old_quantity + _quantity
								session['cart_item'][key]['quantity'] = total_quantity
								session['cart_item'][key]['total_price'] = total_quantity * row['price']
					else:
						session['cart_item'] = array_merge(session['cart_item'], itemArray)
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				else:
					session['cart_item'] = itemArray
					all_total_quantity = all_total_quantity + _quantity
					all_total_price = all_total_price + _quantity * row['price']
				session['all_total_quantity'] = all_total_quantity
				session['all_total_price'] = all_total_price
				return redirect(url_for('.products'))
			else:
				cursor.execute("SELECT * FROM product")
				rows = cursor.fetchall()
				return render_template('index.html', products=rows, status='stock_error')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/')
def products():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM product")
		rows = cursor.fetchall()
		return render_template('index.html', products=rows)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/empty')
def empty_cart():
	try:
		session.pop('all_total_quantity')
		session.pop('all_total_price')
		session.pop('cart_item')
		return redirect(url_for('.displaycart'))
	except Exception as e:
		print(e)

@app.route('/delete/<string:code>')
def delete_product(code):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		for item in session['cart_item'].items():
			if item[0] == code:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		if all_total_quantity == 0:
			session.pop('all_total_quantity')
			session.pop('all_total_price')
			session.pop('cart_item')
		else:
			session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		return redirect(url_for('.displaycart'))
	except Exception as e:
		print(e)
		
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		

@app.route('/search', methods=['POST'])
def search():
	_search = (request.form['search'])
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM product WHERE name LIKE %s OR search_metadata LIKE %s", ("%" + _search + "%","%" + _search + "%",))
		rows = cursor.fetchall()
		if not rows:
			return redirect(url_for('.products'))
		else:
			return render_template('index.html', products=rows)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/transaction', methods=['POST'])
def transaction():
	_pin = int(request.form['pin'])
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT pin FROM user_details where email=%s AND pin=%s",((session["email"]),_pin))
		row_count = cursor.rowcount
		if row_count == 0 :
			return render_template('cart.html', status='pin_error')
		else :
			cursor.execute("SELECT account_balance FROM user_details where email=%s",(session["email"]))
			row = cursor.fetchone()
			balance= float(row['account_balance'])-float(session["all_total_price"])
			balance1=0
			if float(balance) >= float(balance1) :			
				cursor.execute("UPDATE user_details SET account_balance=%s where email=%s",(str(balance),session["email"]))
				conn.commit()
				for key, value in session['cart_item'].items():
					code = session['cart_item'][key]['code']
					cursor.execute("SELECT quantity FROM product WHERE code=%s",code)
					row=cursor.fetchone()
					db_quantity=row['quantity']
					session_quantity = session['cart_item'][key]['quantity']
					new_quantity = int(db_quantity) - int(session_quantity)
					cursor.execute("UPDATE product SET quantity=%s WHERE code=%s",(str(new_quantity),code))
					conn.commit()
				session.pop('all_total_quantity')
				session.pop('all_total_price')  
				session.pop('cart_item')
				return render_template('cart.html', status='success')
			else :
				return render_template('cart.html', status='balance_error')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	return render_template('index.html')

@app.route('/accountUpdate', methods=['POST'])
def accountUpdate():
	update_balance = (request.form['update_balance'])
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT account_balance FROM user_details where email=%s",session["email"])
		row = cursor.fetchone()
		balance = float(row['account_balance'])+float(update_balance)
		cursor.execute("UPDATE user_details SET account_balance=%s where email=%s",(str(balance),session["email"]))
		conn.commit()
		cursor.execute("SELECT user_name, account_balance, pin FROM user_details where email=%s",session["email"])
		row = cursor.fetchone()
		accountInfo = { 'user_name': row['user_name'], 'email': session["email"], 'account_balance': row['account_balance'], 'pin': row['pin'] }
		return render_template('account.html',status='updated',accountInfo=accountInfo)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/signup', methods=['POST'])
def signup():
	cursor = None
	_username = (request.form['user_name'])
	_email = (request.form['email'])
	_password = (request.form['password'])
	_accountbalance = float(500)
	_pin = (request.form['pin'])
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT email FROM user_details WHERE email=%s", _email)
		row_count = cursor.rowcount
		if row_count == 0 :
			insert_statement= ("INSERT INTO user_details VALUES(%s, %s, %s, %s, %s)")
			data= (_username, _email, _password, _accountbalance, _pin)
			cursor.execute(insert_statement,data)
			conn.commit()
			session['email'] = _email
			cursor.execute("SELECT * FROM product")
			rows = cursor.fetchall()
			return render_template('index.html', products=rows, pin= _pin)
		else:
			return render_template('signup.html',status='exists')	
	except Exception as e:
		conn.rollback()
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/signincheck', methods=['POST'])
def signin():
	cursor = None
	_email = (request.form['signin_email'])
	_password = (request.form['signin_password'])
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT email FROM user_details WHERE email=%s AND password=%s",( _email,_password))
		row_count = cursor.rowcount
		if row_count == 0 :
			return render_template('signup.html',status='invalid')
		else:
			session['email'] = _email
			return redirect(url_for('.products'))
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route('/Signin')
def signinpage():
	return render_template('signup.html')

@app.route('/Signout')
def signout():
	try:
		session.clear()
		return redirect(url_for('.products'))
	except Exception as e:
		print(e)

@app.route('/view_cart')
def displaycart():
	return render_template('cart.html')

@app.route('/account')
def account():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT user_name, account_balance, pin FROM user_details where email=%s",session["email"])
		row = cursor.fetchone()
		accountInfo = { 'user_name': row['user_name'], 'email': session["email"], 'account_balance': row['account_balance'], 'pin': row['pin'] }
		return render_template('account.html', accountInfo=accountInfo)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

if __name__ == "__main__":
    app.run(debug=True)