import httpx
from isat.pkg.logger.logger import Logger


class Context:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537.6"
        }
        self.timeout = 3
        self.http_client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)

        self.log = Logger("scraper.log")


ctx = Context()
