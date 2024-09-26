import psycopg2
from psycopg2.extras import NamedTupleCursor
from page_analyzer.models import UrlObject


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
        objects = []
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql)
                entries = cur.fetchall()
        conn.close()
        for entry in entries:
            objects.append(UrlObject(
                id=entry.id,
                name=entry.name,
                created_at=entry.created_at.date(),
            ))
        return objects

    def find(self, id):
        sql = 'SELECT * FROM urls WHERE id = %s;'
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                entry = cur.fetchone()
        conn.close()
        if entry:
            return UrlObject(
                id=entry.id,
                name=entry.name,
                created_at=entry.created_at.date(),
            )
        return None

    def save(self, name):
        id = self.__get_id(name)
        if id:
            return id
        new_object = UrlObject(name)
        sql = '''
            INSERT INTO urls (name, created_at)
            VALUES (%s, %s)
            RETURNING id;
        '''
        conn = self.__get_db_conn()
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_object.name, new_object.created_at))
                id = cur.fetchone()[0]
        conn.close()
        return id
