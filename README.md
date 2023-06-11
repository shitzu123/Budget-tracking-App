# Budget tracking App
It is a simple web application to track monthly budget expenses.
# Key Features
The key features of this application includes
1. The user can signup and login.
2. The user can set monthly income to a prescribed value.
3. The user can add day to day expenses and can find the remaining balance in balance column.
4. In case of any wrong transaction the user can also delete the transaction.
5. The overall expenses history of the user can be found at one place to identify easily.
# Installation Process
1. Clone this Github repo using `git clone https://github.com/shitzu123/Budget-tracking-App.git`
2. Install the dependencies
     + `pip install python`
     + `pip install flask`
     + `pip install flask_mysqldb`
3. After the required installations create two database tables namely signup and income using the following query<br>
   <pre>
   CREATE TABLE signup(
     id INT AUTO-INCREMENT,
     name VARCHAR(20),
     email VARCHAR(30) UNIQUE,
     password VARCHAR(20)
   );</pre>
   <pre>CREATE TABLE income(
     id INT AUTO-INCREMENT,
     user_id INT,
     date DATE,
     username VARCHAR(30),
     text VARCHAR(30),
     amount INT,
     FOREIGN KEY(user_id) REFERENCES signup(id) ON DELETE SET NULL
   );</pre>
4. After the above setup run the "app.py"  file and open in web browser at http://localhost:5000

 
