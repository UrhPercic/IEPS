import psycopg2
from utils import fetch_robots_content, fetch_sitemap_content
from contextlib import contextmanager
import threading

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
        self.lock = threading.Lock()

    @contextmanager
    def get_cursor(self):
        with self.lock:
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
    def fetch_frontier_pages(self, limit=20):
        with self.get_cursor() as cur:
            cur.execute("""
                SELECT id, url FROM crawldb.page WHERE page_type_code = 'FRONTIER' LIMIT %s;
            """, (limit,))
            return cur.fetchall()

    def store_page(self, site_id, page_type_code, url, html_content, http_status_code, accessed_time, content_hash):
        with self.get_cursor() as cur:
            cur.execute("SELECT id FROM crawldb.page WHERE url = %s;", (url,))
            if cur.fetchone():
                print(f"URL already exists in database: {url}")
                return None
            else:
                cur.execute("""
                    INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time, content_hash)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                """, (site_id, page_type_code, url, html_content, http_status_code, accessed_time, content_hash))
                page_id = cur.fetchone()[0]
                return page_id

    def update_page_status(self, page_id, page_type_code, html_content, http_status_code, accessed_time, content_hash):
        with self.get_cursor() as cur:
            cur.execute("""UPDATE crawldb.page SET page_type_code = %s, html_content = %s, http_status_code = %s, accessed_time = %s, content_hash = %s WHERE id = %s;
               """, (page_type_code, html_content, http_status_code, accessed_time, content_hash, page_id))

    def store_page_data(self, page_id, data_type_code, data):
        with self.get_cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO crawldb.page_data (page_id, data_type_code, data)
                    VALUES (%s, %s, %s)
                """, (page_id, data_type_code, data))
            except Exception as e:
                print(f"Error storing page data: {e}")

    def store_images_bulk(self, images):
        with self.get_cursor() as cur:
            insert_query = """
                INSERT INTO crawldb.image (page_id, filename, content_type, data, accessed_time)
                VALUES %s
                ON CONFLICT DO NOTHING;
            """
            from psycopg2.extras import execute_values
            execute_values(cur, insert_query, images)

    def store_pages_bulk(self, pages):
        with self.get_cursor() as cur:
            insert_query = """
                INSERT INTO crawldb.page (site_id, page_type_code, url, html_content, http_status_code, accessed_time, content_hash)
                VALUES %s ON CONFLICT (url) DO NOTHING RETURNING id, url;
            """
            from psycopg2.extras import execute_values
            execute_values(cur, insert_query, pages)
            try:
                page_ids_urls = cur.fetchall()
                return page_ids_urls
            except psycopg2.ProgrammingError:
                return []

    def store_links_bulk(self, links):
        with self.get_cursor() as cur:
            insert_query = """
                INSERT INTO crawldb.link (from_page, to_page)
                VALUES %s
                ON CONFLICT DO NOTHING;
            """
            from psycopg2.extras import execute_values
            execute_values(cur, insert_query, links)

    def check_page_exists(self, url):
        with self.get_cursor() as cur:
            cur.execute("SELECT id FROM crawldb.page WHERE url = %s;", (url,))
            result = cur.fetchone()
            return result[0] if result else None

    def get_robots_content(self, domain):
        with self.get_cursor() as cur:
            cur.execute("SELECT robots_content FROM crawldb.site WHERE domain = %s;", (domain,))
            result = cur.fetchone()
            return result[0] if result else None