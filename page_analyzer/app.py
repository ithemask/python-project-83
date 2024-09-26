from os import getenv
from dotenv import load_dotenv
from page_analyzer.normalizer import normalize
from page_analyzer.validator import is_valid
from page_analyzer.db_access import UrlData
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
DATABASE_URL = getenv('DATABASE_URL')
url_data = UrlData(DATABASE_URL)


@app.get('/')
def index():
    return render_template('index.html', name='')


@app.get('/urls')
def get_urls():
    objects = url_data.get_content()
    return render_template('urls/index.html', objects=objects)


@app.post('/urls')
def post_url():
    name = request.form.get('url')
    if is_valid(name):
        id = url_data.save(normalize(name))
        flash('Страница успешно добавлена')
        return redirect(url_for('show_url', id=id), 302)
    flash('Некорректный URL')
    return render_template('index.html', name=name), 422


@app.get('/urls/<id>')
def show_url(id):
    object = url_data.find(id)
    if object:
        return render_template('urls/show.html', object=object)
    return render_template('not_found.html'), 404
