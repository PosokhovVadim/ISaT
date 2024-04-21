import os
from pkg.models.image import Image


class LocalStorage:
    def __init__(self, directory_path):
        self.directory = directory_path
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

    def save_image(self, data, image: Image):
        with open(image.local_path, "wb") as f:
            f.write(data)
