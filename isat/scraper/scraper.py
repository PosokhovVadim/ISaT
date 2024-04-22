import io
from urllib.parse import urljoin, urlparse
import uuid
from bs4 import BeautifulSoup
import logging
import asyncio
from isat.scraper.context import ctx
from pkg.models.image import Image
from PIL import Image as PILImage  # is ok?
from imagehash import phash

log = logging.getLogger("scraper.log")


async def fetch_url(url):
    response = await ctx.http_client.get(url)
    log.info(f"Fetching {url} : {response.status_code}")
    return response


class Scraper:
    def __init__(self, base_url, allow_domain, max_images):
        self.base_url = base_url
        self.allow_domain = allow_domain
        self.visited_urls = set()
        self.max_images = max_images
        self.total_images = 0
        self.all_images = []

    def make_absolute_url(self, url):
        return urljoin(self.base_url, url)

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    async def scrape_proccess(self, url):
        await self.scrape(url)
        ctx.storage.add_images(self.all_images)

    async def proccess_image(self, image_url):
        response = await fetch_url(image_url)
        if response.status_code != 200:
            log.warning(f"Failed to get image by url: {image_url}")
            return

        content_type = response.headers["content-type"]
        if content_type == "image/jpeg":
            data = response.read()

            if await self.is_duplicate(data):
                log.info(f"Image {image_url} already exists")
                return

            id = str(uuid.uuid4())
            local_path = ctx.local_storage.directory + id + ".png"
            image = Image(id=id, url=image_url, local_path=local_path)

            self.all_images.append(image)
            ctx.local_storage.save_image(data, image)

            self.total_images += 1
            log.info(f"Loaded {image_url}")
            log.info(f"Total images: {self.total_images}")

    async def is_duplicate(self, image_data):
        with io.BytesIO(image_data) as f:
            image = PILImage.open(f)
            img_hash = str(phash(image))

            if ctx.redis.exists(img_hash):
                return True

            ctx.redis.set(img_hash, 1)
            return False

    async def fetch_images(self, soup):
        images_url = [
            img.get("data-src") for img in soup.select("li.slider-item img[data-src]")
        ]

        tasks = []
        for image_url in images_url:
            if image_url is None:
                continue
            tasks.append(self.proccess_image(image_url))
        await asyncio.gather(*tasks)

    async def scrape(self, url):
        if url in self.visited_urls or self.total_images >= self.max_images:
            return

        try:
            response = await fetch_url(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                self.visited_urls.add(url)

                await self.fetch_images(soup)

                for link in soup.find_all("a", href=True):
                    if "data-toggle" in link.attrs and link["data-toggle"] == "modal":
                        continue

                    next_url = self.make_absolute_url(link["href"])
                    if self.get_domain(next_url) != self.allow_domain:
                        continue
                    await self.scrape(next_url)

        except Exception as e:
            log.error(f"Error crawling {url}: {e}")
