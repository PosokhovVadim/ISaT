from io import BytesIO
import io
import logging
import torch
from isat.imageSearch.context import ctx
from PIL import Image as PILImage
from sklearn.metrics.pairwise import cosine_similarity

log = logging.getLogger("image-search.log")


class ImageSearch:
    def __init__(self):
        pass

    def get_tensor(self, img_stream):
        log.info("getting tensor from client image")
        img = PILImage.open(img_stream).convert("RGB")
        tensor = ctx.preprocess(img).unsqueeze(0)

        return tensor

    def get_image_bytes(self, local_path):
        with open(local_path, "rb") as f:
            img = PILImage.open(io.BytesIO(f.read()))
            return img.tobytes()

    def extract_features(self, img_tensor):
        with torch.no_grad():
            features = ctx.model(img_tensor)
        return features.squeeze().numpy()

    def read_blob_to_tensor(self, blob_tensor):
        with BytesIO(blob_tensor) as byte_stream:
            tensor = torch.load(byte_stream)

        return tensor

    async def image_search(self, image, top_n):
        try:
            img_tensor = self.get_tensor(image)
            query_features = self.extract_features(img_tensor)
            images = ctx.storage.get_all_tensors()

            res = []
            for img in images:
                cur_tensor = self.read_blob_to_tensor(img.tensor)
                cur_features = self.extract_features(cur_tensor)

                diff = cosine_similarity([cur_features], [query_features])[0][0]
                img_bytes = self.get_image_bytes(
                    f"{ctx.local_storage.directory}{img.id}.png"
                )

                res.append((img.url, img_bytes, diff))

            res.sort(key=lambda x: x[2], reverse=True)
            return [(img[0], img[1]) for img in res[:top_n]]
        except Exception as e:
            log.error(e)
            return []
