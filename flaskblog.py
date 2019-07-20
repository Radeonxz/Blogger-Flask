from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4e8fc207c81a7969f0e0c098cc50721'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  file_image = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.file_image}')"

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"

posts = [
  {
    'author': 'test1',
    'title': 'title1',
    'content': 'content1',
    'date_posted': '2019-01-01'
  },
  {
    'author': 'test2',
    'title': 'title2',
    'content': 'content2',
    'date_posted': '2019-02-02'
  }
]

@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('home'))
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.email.data == 'admin@admin.com' and form.password.data == 'admin123':
      flash('You have been logged in!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check credentials.', 'danger')
  return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
  app.run(debug=True)