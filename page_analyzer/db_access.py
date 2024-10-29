import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime


def get_db_conn(db_url):
    return psycopg2.connect(db_url)


def get_url_id(conn, url_name):
    sql = 'SELECT id FROM urls WHERE name = %s;'
    with conn.cursor() as cur:
        cur.execute(sql, (url_name,))
        entry = cur.fetchone()
        if entry:
            return entry[0]
        return None


def get_url_info(conn):
    sql = '''
        SELECT DISTINCT ON (u.created_at)
            u.id,
            u.name,
            c.created_at::date,
            c.status_code
        FROM urls u
        LEFT JOIN url_checks c ON u.id = c.url_id
        ORDER BY
            u.created_at DESC,
            c.created_at DESC;
    '''
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def find_url(conn, url_id):
    sql = 'SELECT * FROM urls WHERE id = %s;'
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(sql, (url_id,))
        return cur.fetchone()


def save_url(conn, url_name):
    sql = '''
        INSERT INTO urls (name, created_at)
        VALUES (%s, %s)
        RETURNING id;
    '''
    with conn.cursor() as cur:
        cur.execute(sql, (url_name, datetime.now()))
        return cur.fetchone()[0]


def get_checks(conn, url_id):
    sql = '''
        SELECT * FROM url_checks
        WHERE url_id = %s
        ORDER BY created_at DESC;
    '''
    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(sql, (url_id,))
        return cur.fetchall()


def save_check(conn, check_result):
    sql = '''
        INSERT INTO url_checks (
            url_id,
            status_code,
            h1,
            title,
            description,
            created_at
        )
        VALUES (
            %(url_id)s,
            %(status_code)s,
            %(h1)s,
            %(title)s,
            %(description)s,
            %(created_at)s
        );
    '''
    check_result['created_at'] = datetime.now()
    with conn.cursor() as cur:
        cur.execute(sql, check_result)
