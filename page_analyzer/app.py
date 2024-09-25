import psycopg2
from os import getenv
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
DATABASE_URL = getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    pass


@app.post('/urls')
def post_url():
    pass
