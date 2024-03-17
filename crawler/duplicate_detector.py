from urllib.parse import urljoin, urlparse

class DuplicateDetector:
    def __init__(self, datastore):
        self.datastore = datastore

    def is_duplicate(self, url):
        with self.datastore.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM crawldb.page WHERE url = %s", (url,))
            return cur.fetchone()[0] > 0

    def canonicalize(self, url):
        parsed_url = urlparse(url)
        canonical_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return canonical_url