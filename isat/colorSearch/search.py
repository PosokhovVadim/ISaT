import io
import numpy as np
from isat.colorSearch.context import ctx
from colormath.color_objects import sRGBColor, LabColor, HSVColor
from colormath.color_conversions import convert_color
from PIL import Image as PILImage


class ColorSearch:
    def __init__(self):
        pass

    def euclid_distance(self, color1, color2):
        return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

    def get_image_bytes(self, local_path):
        with open(local_path, "rb") as f:
            img = PILImage.open(io.BytesIO(f.read()))
            return img.tobytes()

    def search_by_lab(self, target_rgb):
        images = ctx.storage.get_all_lab_colors()
        target_lab = convert_color(target_rgb, LabColor)
        res = []
        for img in images:
            curr_color = (img.lab_color_1, img.lab_color_2, img.lab_color_3)
            diff = self.euclid_distance(target_lab.get_value_tuple(), curr_color)
            img_bytes = self.get_image_bytes(
                f"{ctx.local_storage.directory}{img.id}.png"
            )
            res.append((img.url, img_bytes, diff))
        return res

    def search_by_hsv(self, target_rgb):
        images = ctx.storage.get_all_hsv_colors()
        target_hsv = convert_color(target_rgb, HSVColor)
        res = []
        for img in images:
            curr_color = (img.hsv_color_1, img.hsv_color_2, img.hsv_color_3)
            diff = self.euclid_distance(target_hsv.get_value_tuple(), curr_color)
            img_bytes = self.get_image_bytes(
                f"{ctx.local_storage.directory}{img.id}.png"
            )
            res.append((img.url, img_bytes, diff))
        return res

    async def search_process(self, r, g, b, color_space, top_n):
        target_rgb = sRGBColor(r, g, b, is_upscaled=True)
        res = []
        if color_space == "hsv":
            res = self.search_by_hsv(target_rgb)
        elif color_space == "lab":
            res = self.search_by_lab(target_rgb)

        res.sort(key=lambda x: x[2])

        return [(img[0], img[1]) for img in res[:top_n]]
