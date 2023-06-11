from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re 
  
app = Flask(__name__) 
  
app.secret_key = 'abcdef'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'backend'
  
mysql = MySQL(app)
  
@app.route('/')
def startpage():
    return render_template('startpage.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return redirect(url_for('user'))
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/add", methods=['GET', 'POST'])
def add():
    mesage=""
    username = session['name']
    if request.method == 'POST' and 'expense' in request.form and 'amount' in request.form  and 'date' in request.form :
        name = request.form['expense']
        date = request.form['date']
        amount = request.form['amount']
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO income(username,text,amount,user_id,date) VALUES (%s,%s, %s,%s,%s)', (username,name, amount, user_id,date))
        mysql.connection.commit()
        mesage = "Transaction added succesfully"
    return render_template('add.html', mesage=mesage)

@app.route("/history")
def history():
    cursor = mysql.connection.cursor()
    query = """
                SELECT id, income.date, income.text, income.amount
                FROM income
                WHERE user_id = %s and text<>"income"
                ORDER BY date DESC,id DESC
            """
    cursor.execute(query, (session['id'],))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('history.html', data1 = data1)

@app.route('/user', methods=['GET', 'POST'])
def user():
    username = session['name']
    if request.method == 'POST' and 'add' in request.form :
        income = request.form['add']
        name = "income"
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO income(username,text,amount,user_id) VALUES (%s,%s, %s,%s)', (username,name, income, user_id))
        mysql.connection.commit()
    cursor = mysql.connection.cursor()
    query = """
                SELECT SUM(amount)
                FROM income
                WHERE user_id = %s and text<>"income"     
            """
    cursor.execute(query, (session['id'],))
    expense_sum = cursor.fetchone()[0] or 0 
    cursor.close()
    cursor = mysql.connection.cursor()
    query = """
                SELECT id, income.date, income.text, income.amount
                FROM income
                WHERE user_id = %s and text<>"income"
                ORDER BY date DESC,id DESC
                LIMIT 7;
            """
    cursor.execute(query, (session['id'],))
    data1 = cursor.fetchall()
    cursor.close()
    cursor = mysql.connection.cursor()
    query = """
                SELECT amount
                FROM income
                WHERE user_id = %s and text="income" 
                ORDER BY id DESC
                LIMIT 1;
            """
    cursor.execute(query, (session['id'],))
    result = cursor.fetchone()
    if result is not None:
        income_sum = result[0]
    else:
        income_sum = 0
    cursor.close()
    cursor = mysql.connection.cursor()
    query = """
                SELECT(
                (SELECT amount FROM income WHERE text="income" and user_id = %s ORDER BY id DESC LIMIT 1) - (SELECT SUM(amount) FROM income WHERE text<>"income" and user_id=%s)
                )
            """
    cursor.execute(query, (session['id'],session['id']))
    if expense_sum == 0:
        data = income_sum
    else:
        data = cursor.fetchone()[0] or 0
    cursor.close()
    return render_template('user.html', data1 = data1 ,data = data, income_sum=income_sum, expense_sum=expense_sum)

@app.route('/delete', methods=['POST'])
def delete_transaction():
    id = request.form.get('id')
    cursor = mysql.connection.cursor()
    delete_query = "DELETE FROM income WHERE id = %s"
    cursor.execute(delete_query, (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('user'))

@app.route('/remove', methods=['POST'])
def delete_history():
    id = request.form.get('id')
    cursor = mysql.connection.cursor()
    delete_query = "DELETE FROM income WHERE id = %s"
    cursor.execute(delete_query, (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('history'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE name = %s AND email = % s', (userName, email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO signup VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)
    
if __name__ == "__main__":
    app.run(debug=True)