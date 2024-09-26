from psycopg2.extras import NamedTupleCursor
from page_analyzer.models import UrlObject


class UrlData:
    def __init__(self, conn):
        self.conn = conn

    def __get_id(self, name):
        sql = 'SELECT id FROM urls WHERE name = %s;'
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name,))
                entry = cur.fetchone()
                if entry:
                    return entry[0]
                return None

    def get_content(self):
        sql = 'SELECT * FROM urls ORDER BY created_at DESC;'
        objects = []
        with self.conn as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql)
                for entry in cur.fetchall():
                    objects.append(UrlObject(
                        id=entry.id,
                        name=entry.name,
                        created_at=entry.created_at.date(),
                    ))
                return objects

    def find(self, id):
        sql = 'SELECT * FROM urls WHERE id = %s;'
        with self.conn as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
                cur.execute(sql, (id,))
                entry = cur.fetchone()
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
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_object.name, new_object.created_at))
                id = cur.fetchone()[0]
                return id
