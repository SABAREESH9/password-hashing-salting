import re
import secrets
from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

users = {}
login_attempts = {}

def hash_password(password, salt):
    # Dummy implementation of password hashing. Replace with a secure hashing algorithm like bcrypt.
    return salt + password.encode('utf-8')

def verify_password(stored_password, password):
    # Dummy implementation of password verification. Adjust according to your hash_password function.
    salt = stored_password[:16]
    return stored_password == salt + password.encode('utf-8')

def password_strength(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[^A-Za-z0-9]", password):
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        if not password_strength(password):
            return 'Password strength error: Password is not strong enough!'
        else:
            salt = secrets.token_bytes(16)
            hashed_password = hash_password(password, salt)
            if username not in users:
                users[username] = hashed_password
                return 'Registered successfully!'
            else:
                return 'Username already exists'
    except Exception as e:
        return str(e)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username not in login_attempts:
        login_attempts[username] = 0

    login_attempts[username] += 1
    if login_attempts[username] > 3:
        return 'Account locked due to excessive login attempts!'

    if username in users:
        if verify_password(users[username], password):
            session['username'] = username
            login_attempts[username] = 0
            return 'Logged in successfully!'

    return 'Invalid username or password'

if __name__ == '__main__':
    app.run(debug=True)
