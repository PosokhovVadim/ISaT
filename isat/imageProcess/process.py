# TODO: IMPLEMENT
# 1) save images without background
# 2) count color for every empty_bg images
# 3) count tensors

import asyncio
import os
from isat.imageProcess.context import ctx
from PIL import Image as PILImage
from rembg import remove
import numpy as np
from skimage.color import rgb2lab, rgb2hsv


import logging


log = logging.getLogger("scraper.log")


class ImageProcess:
    def __init__(self):
        self.local_storage = ctx.local_storage
        self.empty_bg_storage = ctx.local_empty_bg_storage

    async def remove_bg(self, filename):
        img = PILImage.open(self.local_storage.directory + filename)
        new_img = remove(img)
        new_img.save(self.empty_bg_storage.directory + filename)

    async def get_mean_color(self, filename):
        img = PILImage.open(self.local_storage.directory + filename)
        np_array = np.array(img)
        rgb_array = np_array[:, :, :3]

        mask = np_array[:, :, 3] > 0
        rgb_array_masked = rgb_array[mask]

        lab_array_masked = rgb2lab(rgb_array_masked)
        mean_lab_color = np.mean(lab_array_masked, axis=(0))

        hsv_array_masked = rgb2hsv(rgb_array_masked)
        mean_hsv_color = np.mean(hsv_array_masked, axis=(0))

        return filename.rsplit(".", 1)[0], mean_lab_color, mean_hsv_color

    async def count_tensor(self):
        pass

    async def image_process(self):
        # bg process + count tensor

        bg_tasks = []
        for filename in os.listdir(self.local_storage.directory):
            bg_tasks.append(self.remove_bg(filename))
        await asyncio.gather(*bg_tasks)

        # count process
        cl_tasks = []
        for filename in os.listdir(self.empty_bg_storage.directory):
            cl_tasks.append(self.get_mean_color(filename))
        colors = await asyncio.gather(*cl_tasks)

        for id, lab_color, hsv_color in colors:
            ctx.storage.update(id, lab_color, hsv_color)
