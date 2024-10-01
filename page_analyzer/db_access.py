import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime


class UrlData:
    def __init__(self, db_url):
        self.db_url = db_url

    def __get_db_conn(self):
        return psycopg2.connect(self.db_url)

    def get_url_id(self, name):
        sql = 'SELECT id FROM urls WHERE name = %s;'
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                entry = cur.fetchone()
        conn.close()
        if entry:
            return entry[0]
        return None

    def get_main_info(self):
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
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql)
                entries = cur.fetchall()
        conn.close()
        return entries

    def find_url(self, id):
        sql = 'SELECT * FROM urls WHERE id = %s;'
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                entry = cur.fetchone()
        conn.close()
        return entry

    def save_url(self, name):
        sql = '''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            RETURNING id;
        '''
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name, datetime.now()))
                id = cur.fetchone()[0]
        conn.close()
        return id

    def get_checks(self, id):
        sql = '''
            SELECT * FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC;
        '''
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                entries = cur.fetchall()
        conn.close()
        return entries

    def save_check(self, check_result):
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
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, check_result)
        conn.close()
        return
