import httpx
import os
from isat.pkg.logger.logger import Logger
from isat.pkg.storage.local.local import Local_Storage
from isat.pkg.storage.sqllite.sqllite import Storage


class Context:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537.6"
        }
        self.timeout = 3

        self.http_client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        self.log = Logger("scraper.log")

        self.local_storage = Local_Storage("images/")

        sqllite_path = os.getenv("SQLITE_DATABASE")
        self.storage = Storage(sqllite_path)


ctx = Context()
