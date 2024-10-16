from psycopg2.extras import NamedTupleCursor
from datetime import datetime


class UrlData:
    def get_url_id(self, conn, name):
        sql = 'SELECT id FROM urls WHERE name = %s;'
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                entry = cur.fetchone()
                if entry:
                    return entry[0]
                return None

    def get_main_info(self, conn):
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
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql)
                return cur.fetchall()

    def find_url(self, conn, id):
        sql = 'SELECT * FROM urls WHERE id = %s;'
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                return cur.fetchone()

    def save_url(self, conn, name):
        sql = '''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            RETURNING id;
        '''
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name, datetime.now()))
                return cur.fetchone()[0]

    def get_checks(self, conn, id):
        sql = '''
            SELECT * FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC;
        '''
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                return cur.fetchall()

    def save_check(self, conn, check_result):
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
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, check_result)
                return
