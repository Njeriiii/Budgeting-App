from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8d1b7db110d988e1b13b9656df9655af'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def _repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def _repr__(self):
        return f"Post('{self.category}', '{self.amount}', '{self.date_posted}')"




all_expenses = [
    {
        "id":1,
        "title":"Headphones",
        "category":"Electronics",
        "amount":100,
        "date": datetime.strptime("22-02-2019", '%d-%m-%Y')
    },
    {
        "id":2,
        "title":"BBQ and Bacons",
        "category":"Food",
        "amount":200,
        "date":datetime.strptime("12-09-2019", '%d-%m-%Y')
    },
    {
        "id":3,
        "title":"Spotify",
        "category":"Sevices",
        "amount":15,
        "date":datetime.strptime("23-08-2019", '%d-%m-%Y')
    },
    {
        "id":4,
        "title":"Netflix",
        "category":"Sevices",
        "amount":30,
        "date":datetime.strptime("23-12-2019", '%d-%m-%Y')
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title = "About Page")

@app.route("/transactions")
def transactions():
    return render_template('transactions.html', expenses=all_expenses)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data} successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        flash('You have been logged in!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
