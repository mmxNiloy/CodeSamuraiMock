from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYSECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.app_context().push()

db = SQLAlchemy(app)


from routes import *


if __name__ == '__main__':
    app.run(debug=True)