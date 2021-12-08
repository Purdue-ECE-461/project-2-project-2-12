from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

# initialising the flask app
app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'whatisasecretkeyonemayask'

db = SQLAlchemy(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@/{}?unix_socket=/cloudsql/{}".format(
#     'prembhanderi', 'justguess', 'mydatabase', 'ece-461-pyapi:us-east1:project2-mysql-database')

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://prembhanderi:justguess@localhost:3306/mydatabase"


class UserModel(db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255), primary_key=True, index=True)
    password = db.Column(db.String(255))
    isAdmin = db.Column(db.Boolean)


class PackageModel(db.Model):
    __tablename__ = 'packages'
    name = db.Column(db.String(255))
    version = db.Column(db.String(255))
    id = db.Column(db.String(255), primary_key=True)
    url = db.Column(db.String(255))
    content = db.Column(db.Text)
    action = db.Column(db.String(255))
    actionTime = db.Column(db.String(255))
