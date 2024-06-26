import yaml
import logging

log = logging.getLogger("scraper.log")


class Config:
    def __init__(self, config_path):
        self.config = self.readConfig(config_path)
        self.allow_domain = self.config["allow_domain"]
        self.base_url = self.config["base_url"]
        self.host = self.config["http_server"]["host"]
        self.port = self.config["http_server"]["port"]

    def readConfig(self, config_path):
        try:
            with open(config_path, "r") as config_file:
                log.info("Reading config file successfully")
                return yaml.safe_load(config_file)
        except IOError:
            log.error("Config file not found")
            raise IOError
