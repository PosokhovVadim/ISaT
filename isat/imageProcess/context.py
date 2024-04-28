import httpx
import os
from pkg.logger.logger import Logger
from pkg.storage.local.local import LocalStorage
from pkg.storage.sqllite.sqllite import Storage
import torchvision.transforms as transforms


class Context:
    def __init__(self):
        self.http_client = httpx.AsyncClient()
        self.log = Logger("image-process.log")

        self.local_storage = LocalStorage("images/")
        self.local_empty_bg_storage = LocalStorage("images_empty_bg/")

        sqllite_path = os.getenv("SQLITE_DATABASE")

        self.storage = Storage(sqllite_path)

        self.preprocess = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )


ctx = Context()
