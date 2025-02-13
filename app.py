from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "7845036121"  # Change this to a secure key

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://kuhanm:*****@cluster0.uagdz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tls=True, tlsAllowInvalidCertificates=True)  # Replace with your actual connection string
db = client["user_auth"]
users_collection = db["users"]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        flash("Some fields are missing.")
        return redirect(url_for('home'))

    if users_collection.find_one({'email': email}):
        flash("Email already registered. Please log in.")
        return redirect(url_for('home'))

    hashed_password = generate_password_hash(password)  # Hash the password
    users_collection.insert_one({'username': username, 'email': email, 'password': hashed_password})

    flash("Sign-up successful! Please log in.")
    return redirect(url_for('home'))

@app.route('/signin', methods=['POST'])
def signin():
    email = request.form.get('email')
    password = request.form.get('password')

    # Find user in database
    user = users_collection.find_one({'email': email})

    if user and check_password_hash(user['password'], password):  # Verify hashed password
        session['username'] = user['username']  # Store username in session
        return redirect(url_for('dashboard'))  # Redirect to dashboard

    flash("Invalid credentials. Try again.")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('home'))  # Redirects user to login if not logged in

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('home'))  # Redirect to login page

if __name__ == "__main__":
    app.run(debug=True)
