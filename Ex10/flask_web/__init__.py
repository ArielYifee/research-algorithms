# Here, we add a secret key:

from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ecf6e975838a2f7bf3c5dbe7d55ebe5b'  ###

# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
# db = SQLAlchemy(app)

from flask_web import routes

