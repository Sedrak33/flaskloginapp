from flask import Flask, render_template, request, redirect, url_for, flash
import re
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Function to validate email format
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

# Function to validate password strength
def is_valid_password(password):
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

# Path to the user data file
USER_DATA_FILE = 'users.txt'
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate email and password
        if not email or not is_valid_email(email):
            flash('Invalid email address.')
            return redirect(url_for('signup'))
        if not password or not is_valid_password(password):
            flash('Password must be at least 12 characters and include at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol.')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save the user data
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f"{email},{username},{hashed_password.decode('utf-8')}\n")

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate login credentials
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                stored_email, username, stored_hashed_password = line.strip().split(',')
                if stored_email == email and bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    return render_template('success.html')

        flash('Invalid email or password.')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
