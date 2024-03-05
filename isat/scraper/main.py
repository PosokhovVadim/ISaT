from fastapi import FastAPI
from isat.pkg.logger.logger import Logger
from isat.scraper.config.config import Config
from isat.scraper import crawler

app = FastAPI()
log = Logger("scraper.log")


# for instance
@app.get("/scrap")
def read_root():
    # implement is later
    log.info("Start scraping")
    return {"Service": "1"}


def main():
    log.info("Starting scraper service")

    # cfg = Config(os.getenv("CONFIG_PATH"))
    cfg = Config("isat/scraper/config/config.yaml")

    crw = crawler.Crawler(
        cfg.base_url, cfg.allow_domain, "isat/scraper/config/urls_data.json"
    )

    crw.crawl()
    # log.info(f"Config: {cfg.host}:{cfg.port}")
    # uvicorn.run("isat.scraper.main:app", host=cfg.host, port=cfg.port, reload=True)


# todo:
# 1) Implement logger - done
# 2) create cofig  - sooo, why??? - done
# 3) Implement crowler (async ???) - done without async
# 4) Implement scraper (where contain img, check async impl.) thats all?)
