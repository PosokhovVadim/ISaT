import os
from isat.pkg.models.image import Image


class Local_Storage:
    def __init__(self, directory_path):
        self.directory = directory_path
        if os.path.exists(self.directory) is False:
            os.mkdir(self.directory)

    def save_image(self, data, image: Image):
        with open(image.local_path, "wb") as f:
            f.write(data)
