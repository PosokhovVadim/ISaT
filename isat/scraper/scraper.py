from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
import asyncio
from isat.scraper.context import ctx

log = logging.getLogger("scraper.log")


async def fetch_url(url):
    response = await ctx.http_client.get(url)
    log.info(f"Fetching {url} : {response.status_code}")
    return response


class Scraper:
    def __init__(self, base_url, allow_domain, max_images=1000):
        self.base_url = base_url
        self.allow_domain = allow_domain
        self.visited_urls = set()
        self.max_images = max_images
        self.total_images = 0

    def make_absolute_url(self, url):
        return urljoin(self.base_url, url)

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    async def save_images(self, image_url):
        # respone = await fetch_url(image_url)
        # log.info(f"Saving {image_url} : {respone.status_code}")
        # if respone.status_code != 200:
        #     log.warning(f"Failed to load {image_url}")
        #     return

        self.total_images += 1
        log.info(f"Loaded {image_url}")
        log.info(f"Total images: {self.total_images}")
        # todo: local save
        # todo: save to db

    async def processing_images(self, soup):
        images_url = [
            img.get("data-src") for img in soup.select("li.slider-item img[data-src]")
        ]
        tasks = []
        for image_url in images_url:
            if image_url is None:
                continue
            tasks.append(self.save_images(image_url))
        await asyncio.gather(*tasks)

    async def scrape(self, url):
        if url in self.visited_urls or self.total_images >= self.max_images:
            return

        try:
            response = await fetch_url(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                self.visited_urls.add(url)

                await self.processing_images(soup)

                log.info(f"Scraped {url}")
                log.info(f"Total visited: {len(self.visited_urls)}")
                for link in soup.find_all("a", href=True):
                    if "data-toggle" in link.attrs and link["data-toggle"] == "modal":
                        continue

                    next_url = self.make_absolute_url(link["href"])
                    if self.get_domain(next_url) != self.allow_domain:
                        continue
                    await self.scrape(next_url)

        except Exception as e:
            log.error(f"Error crawling {url}: {e}")
