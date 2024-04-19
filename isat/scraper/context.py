import httpx
import os
from pkg.logger.logger import Logger
from pkg.storage.local.local import LocalStorage
from pkg.storage.sqllite.sqllite import Storage
import redis


class Context:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.112 Safari/537.6"
        }
        self.timeout = 3

        self.http_client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        self.log = Logger("scraper.log")

        self.local_storage = LocalStorage("images/")

        sqllite_path = os.getenv("SQLITE_DATABASE")
        redis_path = os.getenv("REDIS_PATH")

        self.storage = Storage(sqllite_path)
        self.redis = redis.Redis.from_url(redis_path)


ctx = Context()
