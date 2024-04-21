import httpx
import os
from pkg.logger.logger import Logger
from pkg.storage.local.local import LocalStorage
from pkg.storage.sqllite.sqllite import Storage


class Context:
    def __init__(self):
        self.http_client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        self.log = Logger("image-process.log")

        self.local_storage = LocalStorage("images/")
        self.local_empty_bg_storage = LocalStorage("images_empty_bg/")

        sqllite_path = os.getenv("SQLITE_DATABASE")

        self.storage = Storage(sqllite_path)


ctx = Context()
