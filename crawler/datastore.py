import psycopg2
from utils import fetch_robots_content, fetch_sitemap_content
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
                robots_content = fetch_robots_content(domain)
                sitemap_content = fetch_sitemap_content(domain)

                cur.execute("""
                    INSERT INTO crawldb.site (domain, robots_content, sitemap_content)
                    VALUES (%s, %s, %s) RETURNING id;
                """, (domain, robots_content, sitemap_content))

                return cur.fetchone()[0]

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

    def store_link(self, from_page_id, to_page_id):
        with self.get_cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO crawldb.link (from_page, to_page)
                    VALUES (%s, %s)
                    """, (from_page_id, to_page_id))
            except Exception as e:
                print(f"Error storing link: {e}")

    def check_page_exists(self, url):
        with self.get_cursor() as cur:
            cur.execute("SELECT id FROM crawldb.page WHERE url = %s;", (url,))
            result = cur.fetchone()
            return result[0] if result else None