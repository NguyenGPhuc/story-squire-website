from flask import Flask, render_template, request, session, redirect, url_for
import MySQLdb
from ignore_this import config
import secrets

app = Flask(__name__)

# Set secret key for session management
app.secret_key = config.secret_key

# Set up database connection parameters
db_endpoint = config.DB_ENDPOINT
db_username = config.DB_USERNAME
db_password =  config.DB_PASSWORD
db_name = config.DB_NAME

# Create a connection object to database
com = MySQLdb.connect(host=db_endpoint, user=db_username, passwd=db_password, db=db_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', method=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = com.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        com.commit()
        cursor.close()

        session['username'] = username

        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        cursor = com.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error='Invalid username or password')

    return render_template('signin.html')

@app.route('/', methods=['POST'])
def process_text():
    user_text = request.form['user_text']
    return f'You entered: {user_text}'

if __name__ == '__main__':
    app.run(debug=True)
