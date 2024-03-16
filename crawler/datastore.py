import psycopg2
from psycopg2 import sql
from contextlib import contextmanager

class DataStore:
    def __init__(self, dbname='postgres', user='postgres', password='12345', host='localhost', port=5432):
        self.conn_details = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.conn = psycopg2.connect(**self.conn_details)
        self.conn.autocommit = True

    @contextmanager
    def get_cursor(self):
        """Context manager for getting a cursor and automatically closing it."""
        cursor = self.conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def get_or_create_site_id(self, domain):
        with self.get_cursor() as cur:
            cur.execute("SELECT id FROM crawldb.site WHERE domain = %s;", (domain,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                cur.execute("INSERT INTO crawldb.site (domain) VALUES (%s) RETURNING id;", (domain,))
                return cur.fetchone()[0]  # No need to call commit due to autocommit

    def store_page(self, site_id, page_type_code, url, html_content, http_status_code, accessed_time):
        with self.get_cursor() as cur:
            cur.execute("""
                INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                """, (site_id, page_type_code, url, html_content, http_status_code, accessed_time))
            page_id = cur.fetchone()[0]
            return page_id

    def store_image(self, page_id, filename, content_type, data, accessed_time):
        with self.get_cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (page_id, filename, content_type, data, accessed_time))
            except Exception as e:
                print(f"Error storing image: {e}")

    def store_link(self, from_page, to_page):
        with self.get_cursor() as cur:
            cur.execute("""
                INSERT INTO crawldb.link (from_page, to_page)
                VALUES (%s, %s)
                """, (from_page, to_page))

    def check_page_exists(self, url):
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT id FROM crawldb.page WHERE url = %s
                """, (url,))
            return cur.fetchone() is not None
