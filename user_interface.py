from flask import Flask, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'super secret key'
users = {'user1': 'pass1', 'user2': 'pass2'}  # Replace with database
print("App initialized")
@app.route('/login', methods=['POST'])
def login():
    print("Login route reached")
    username = request.form['username']
    password = request.form['password']
    print(f"Username: {username}, Password: {password}")
    if username in users and users[username] == password:
        print("Login successful")
        session['username'] = username
        return redirect(url_for('home'))
    print("Invalid username or password")
    return 'Invalid username or password'
@app.route('/', methods=['GET', 'POST'])
def login_register():
    print("Route reached")
    if request.method == 'POST':
        print("Form submitted")
        action = request.form['action']
        if action == 'login':
            return redirect(url_for('login'))
        elif action == 'register':
            username = request.form['username']
            password = request.form['password']
            if username not in users:
                print("User registered successfully")
                users[username] = password
                return 'User registered successfully!'
            print("Username already exists")
            return 'Username already exists'
    print("GET request")
    return '''
    <form action="" method="post">
      <input type="text" name="username" placeholder="Username">
      <input type="password" name="password" placeholder="Password">
      <input type="submit" name="action" value="Login">
      <input type="submit" name="action" value="Register">
    </form>
    '''
@app.route('/home')
def home():
    print("Home route reached")
    if 'username' in session:
        print("User logged in")
        return f'Welcome {session["username"]}!'
    print("User not logged in")
    return 'You are not logged in'
@app.route('/logout')
def logout():
    print("Logout route reached")
    session.pop('username', None)
    print("User logged out")
    return redirect(url_for('login_register'))
if __name__ == '__main__':
    print("App running")
    app.run(debug=True)