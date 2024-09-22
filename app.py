from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Path to the user data file
USER_DATA_FILE = 'users.txt'

# Function to save user data
def save_user(email, username, hashed_password):
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{email},{username},{hashed_password.decode()}\n")

# Function to check if user exists
def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.split(',')[1] == username:
                return True
    return False

# Function to validate password
def validate_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if user_exists(username):
            flash('Username already exists. Please choose another.')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        save_user(email, username, hashed_password)
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                email, stored_username, stored_password = line.strip().split(',')
                if stored_username == username:
                    if validate_password(stored_password, password):
                        flash('Login successful!')
                        return render_template('success.html')
                    else:
                        flash('Invalid password. Please try again.')
                        return redirect(url_for('login'))

        flash('Username not found. Please register.')
        return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
