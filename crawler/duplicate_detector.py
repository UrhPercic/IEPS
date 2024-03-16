class DuplicateDetector:
    def __init__(self, datastore):
        self.datastore = datastore

    def is_duplicate(self, url):
        with self.datastore.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM crawldb.page WHERE url = %s", (url,))
            return cur.fetchone()[0] > 0
