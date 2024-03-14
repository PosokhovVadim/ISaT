from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

import requests

log = logging.getLogger("scraper.log")


class Scraper:
    def __init__(self, base_url, allow_domain, data_path, max_images=1000):
        self.base_url = base_url
        self.allow_domain = allow_domain
        self.data_path = data_path
        self.visited_urls = set()
        self.max_images = max_images
        self.total_images = 0

    def make_absolute_url(self, url):
        return urljoin(self.base_url, url)

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def extract_images(self, soup):
        images = [
            img.get("data-src") for img in soup.select("li.slider-item img[data-src]")
        ]

        self.total_images += len(images)
        log.info(f"total_images: {self.total_images}")
        log.info(f"len images: {len(images)}")

    def save_images(self, soup):
        self.extract_images(soup)
        # save to db

    def scrape(self, url):
        if url in self.visited_urls or self.total_images >= self.max_images:
            return

        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                self.visited_urls.add(url)

                self.save_images(soup)

                log.info(f"Scraped {url}")
                for link in soup.find_all("a", href=True):
                    if "data-toggle" in link.attrs and link["data-toggle"] == "modal":
                        continue

                    next_url = self.make_absolute_url(link["href"])
                    if self.get_domain(next_url) != self.allow_domain:
                        continue
                    self.scrape(next_url)

        except Exception as e:
            log.error(f"Error crawling {url}: {e}")
