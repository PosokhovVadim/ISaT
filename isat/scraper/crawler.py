import json
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging

import requests

log = logging.getLogger("scraper.log")


class Crawler:
    def __init__(self, base_url, allow_domain, data_path, save_interval=10):
        self.base_url = base_url
        self.allow_domain = allow_domain
        self.data_path = data_path
        self.save_interval = save_interval
        self.last_save_time = time.time()
        self.visited_urls = {}

    def crawl(self):
        self.crawler(self.base_url)

    def load_visited_data(self):
        try:
            with open(self.data_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_visited_data(self, incremental=False):
        if incremental:
            existing_data = self.load_visited_data()
            existing_data.update(self.visited_urls)
            data_to_save = existing_data
        else:
            data_to_save = self.visited_urls

        with open(self.data_path, "w") as file:
            json.dump(data_to_save, file, indent=2)

    def make_absolute_url(self, url):
        return urljoin(self.base_url, url)

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def crawler(self, url):
        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # todo: fix img
                # image_urls = [img['src'] for img in soup.find_all('img', src=True)]
                self.visited_urls[url] = "added"
                log.info(f"Crawled: {url}")

                if time.time() - self.last_save_time > self.save_interval:
                    self.save_visited_data(incremental=True)
                    self.last_save_time = time.time()

                for link in soup.find_all("a", href=True):
                    next_url = self.make_absolute_url(link["href"])
                    if self.get_domain(next_url) != self.allow_domain:
                        continue
                    self.crawler(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

        self.save_visited_data()
