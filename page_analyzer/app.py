from os import getenv
from dotenv import load_dotenv
from page_analyzer.normalizer import normalize
from page_analyzer.validator import is_valid
from page_analyzer.db_access import UrlData
from page_analyzer.check import check
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['DATABASE_URL'] = getenv('DATABASE_URL')
url_data = UrlData(app.config['DATABASE_URL'])


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    records = url_data.get_main_info()
    return render_template('urls/index.html', records=records)


@app.post('/urls')
def post_url():
    name = request.form.get('url')
    if not is_valid(name):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', name=name), 422
    name = normalize(name)
    id = url_data.get_url_id(name)
    if id:
        flash('Страница уже существует', 'info')
    else:
        id = url_data.save_url(name)
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_url', id=id), 302)


@app.get('/urls/<id>')
def show_url(id):
    url = url_data.find_url(id)
    if url:
        checks = url_data.get_checks(id)
        return render_template('urls/show.html', url=url, checks=checks)
    abort(404)


@app.post('/urls/<id>/checks')
def check_url(id):
    name = request.args.get('name')
    check_result = check(name)
    if check_result:
        check_result['url_id'] = id
        url_data.save_check(check_result)
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('show_url', id=id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('server_error.html'), 500
