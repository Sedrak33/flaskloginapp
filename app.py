from flask import Flask, render_template, request, redirect, url_for
import re  # Import regular expressions for password validation

app = Flask(__name__)

# Function to check if the password meets the criteria
def is_valid_password(password):
    if (len(password) >= 12 and 
        re.search(r"[A-Z]", password) and  # At least one uppercase letter
        re.search(r"[a-z]", password) and  # At least one lowercase letter
        re.search(r"[0-9]", password) and  # At least one number
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):  # At least one symbol
        return True
    return False

# Function to check if user exists and validate password
def validate_login(username, password):
    try:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            for user in users:
                stored_user, stored_password = user.strip().split(',')
                if stored_user == username and stored_password == password:
                    return True
    except FileNotFoundError:
        pass
    return False

# Function to register a new user
def register_user(username, password):
    with open('users.txt', 'a') as file:
        file.write(f'{username},{password}\n')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if validate_login(username, password):
        return redirect(url_for('success'))
    else:
        return "Login failed. Please try again."

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the password is valid
    if not is_valid_password(password):
        return "Password must be at least 12 characters long and contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 symbol."
    
    register_user(username, password)
    return "User registered successfully!"

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
