from os import getenv
from dotenv import load_dotenv
from flask import (
    Flask,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
