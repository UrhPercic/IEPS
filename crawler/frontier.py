from queue import Queue

class URLFrontier:
    def __init__(self):
        self.frontier = Queue()

    def add_url(self, url):
        self.frontier.put(url)

    def get_url(self):
        return self.frontier.get()

    def empty(self):
        return self.frontier.empty()