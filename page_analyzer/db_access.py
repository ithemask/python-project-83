import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime


class UrlData:
    def __init__(self, db_url):
        self.db_url = db_url

    def __get_db_conn(self):
        return psycopg2.connect(self.db_url)

    def __get_id(self, name):
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

    def get_content(self):
        sql = 'SELECT * FROM urls ORDER BY created_at DESC;'
        conn = self.__get_db_conn()
        urls = []
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql)
                entries = cur.fetchall()
        conn.close()
        for entry in entries:
            urls.append(entry)
        return urls

    def find(self, id):
        sql = 'SELECT * FROM urls WHERE id = %s;'
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                entry = cur.fetchone()
        conn.close()
        return entry

    def save(self, name):
        id = self.__get_id(name)
        if id:
            return id
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
