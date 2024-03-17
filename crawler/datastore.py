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
            cur.execute("SELECT id FROM crawldb.page WHERE url = %s;", (url,))
            if cur.fetchone():
                print(f"URL already exists in database: {url}")
                return None
            else:
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

    def store_link_from_urls(self, from_url, to_url):
        with self.get_cursor() as cur:
            try:
                cur.execute("SELECT id FROM crawldb.page WHERE url = %s", (from_url,))
                from_page_id = cur.fetchone()
                if not from_page_id:
                    print(f"From URL not found in database: {from_url}")
                    return

                cur.execute("SELECT id FROM crawldb.page WHERE url = %s", (to_url,))
                to_page_id = cur.fetchone()
                if not to_page_id:
                    print(f"To URL not found in database: {to_url}")
                    return

                cur.execute("""
                    INSERT INTO crawldb.link (from_page, to_page)
                    VALUES (%s, %s)
                    """, (from_page_id[0], to_page_id[0]))
            except Exception as e:
                print(f"Error storing link: {e}")

