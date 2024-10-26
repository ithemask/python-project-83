from os import getenv
from dotenv import load_dotenv
from page_analyzer import db_access
from page_analyzer.normalizer import normalize
from page_analyzer.validator import is_valid
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


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def get_urls():
    conn = db_access.get_db_conn(app.config['DATABASE_URL'])
    with conn:
        url_info = db_access.get_url_info(conn)
        response = render_template('urls/index.html', url_info=url_info)
    conn.close()
    return response


@app.post('/urls')
def post_url():
    conn = db_access.get_db_conn(app.config['DATABASE_URL'])
    with conn:
        url_name = request.form.get('url')
        if not is_valid(url_name):
            flash('Некорректный URL', 'danger')
            response = render_template('index.html', url_name=url_name), 422
        else:
            url_name = normalize(url_name)
            url_id = db_access.get_url_id(conn, url_name)
            if url_id:
                flash('Страница уже существует', 'info')
            else:
                url_id = db_access.save_url(conn, url_name)
                flash('Страница успешно добавлена', 'success')
            response = redirect(url_for('show_url', url_id=url_id), 302)
    conn.close()
    return response


@app.get('/urls/<url_id>')
def show_url(url_id):
    conn = db_access.get_db_conn(app.config['DATABASE_URL'])
    with conn:
        url = db_access.find_url(conn, url_id)
        if url:
            checks = db_access.get_checks(conn, url_id)
            response = render_template(
                'urls/show.html',
                url=url,
                checks=checks,
            )
        else:
            response = abort(404)
    conn.close()
    return response


@app.post('/urls/<url_id>/checks')
def check_url(url_id):
    conn = db_access.get_db_conn(app.config['DATABASE_URL'])
    with conn:
        url_name = request.args.get('url_name')
        check_result = check(url_name)
        if check_result:
            check_result['url_id'] = url_id
            db_access.save_check(conn, check_result)
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'danger')
        response = redirect(url_for('show_url', url_id=url_id))
    conn.close()
    return response


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('server_error.html'), 500
