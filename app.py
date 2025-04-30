from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'adham0544'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists!"
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "Signup successful"
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return f"Welcome back, {user.username}!"
        else:
            return "Invalid username or password."
    #     user = User.query.filter_by(username=username, password=password).first()
    #     if user:
    #         session['user_id'] = user.id
    #         return redirect(url_for('dashboard'))
    # return redirect(url_for('login'))

@app.route('/dashboard' , methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)


