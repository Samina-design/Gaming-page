   from flask import Flask, render_template, request, redirect, url_for, flash
   from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
   import sqlite3
   from werkzeug.security import generate_password_hash, check_password_hash
   import requests

   app = Flask(__name__)
   app.secret_key = 'your_secret_key'
   login_manager = LoginManager()
   login_manager.init_app(app)

   class User(UserMixin):
       def __init__(self, id, username, password):
           self.id = id
           self.username = username
           self.password = password

   @login_manager.user_loader
   def load_user(user_id):
       conn = sqlite3.connect('database.db')
       cursor = conn.cursor()
       cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
       user_data = cursor.fetchone()
       conn.close()
       if user_data:
           return User(user_data[0], user_data[1], user_data[2])
       return None

   def init_db():
       conn = sqlite3.connect('database.db')
       cursor = conn.cursor()
       cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
       conn.commit()
       conn.close()

   @app.route('/')
   def index():
       return render_template('index.html')

   @app.route('/login', methods=['GET', 'POST'])
   def login():
       if request.method == 'POST':
           username = request.form['username']
           password = request.form['password']
           conn = sqlite3.connect('database.db')
           cursor = conn.cursor()
           cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
           user_data = cursor.fetchone()
           conn.close()
           if user_data and check_password_hash(user_data[2], password):
               user = User(user_data[0], user_data[1], user_data[2])
               login_user(user)
               return redirect(url_for('index'))
           flash('Invalid credentials')
       return render_template('login.html')

   @app.route('/signup', methods=['GET', 'POST'])
   def signup():
       if request.method == 'POST':
           username = request.form['username']
           password = generate_password_hash(request.form['password'])
           conn = sqlite3.connect('database.db')
           cursor = conn.cursor()
           cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
           conn.commit()
           conn.close()
           flash('Account created successfully')
           return redirect(url_for('login'))
       return render_template('signup.html')

   @app.route('/logout')
   @login_required
   def logout():
       logout_user()
       return redirect(url_for('index'))

   if __name__ == '__main__':
       init_db()
       app.run(debug=True)


@app.route('/news')
   def news():
       response = requests.get('https://example.com/api/gaming-news')
       news_data = response.json()
       return render_template('news.html', news=news_data)
