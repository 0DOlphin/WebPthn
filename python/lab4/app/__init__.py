from flask import Flask

app = Flask(__name__)
app.secret_key="rsCbvb5ke2reU52f7kNSg2jw"

from app import views
