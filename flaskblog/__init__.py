from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import Loginmanager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4e8fc207c81a7969f0e0c098cc50721'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = Loginmanager(app)

from flaskblog import routes