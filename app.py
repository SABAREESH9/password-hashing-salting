from flask import Flask, request, redirect, url_for, session, render_template

app = Flask(__name__)
app.secret_key = 'secret_key'

users = {'user1': 'pass1'}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        session['username'] = username
        return 'Logged in successfully!'
    return 'Invalid username or password'

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username not in users:
        users[username] = password
        return 'Registered successfully!'
    return 'Username already exists'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logged out successfully!'

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/loginform')
def loginform():
    return render_template('login.html')

@app.route('/registerform')
def registerform():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

