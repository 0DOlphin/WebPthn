from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fsCdvb3kb2Dep1gfdkFSD2Fw'

from app import views
