from fastapi import FastAPI
from isat.pkg.logger.logger import Logger
from isat.scraper.config.config import Config
from isat.scraper import scraper

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

    scr = scraper.Scraper(
        cfg.base_url, cfg.allow_domain, "isat/scraper/config/urls_data.json"
    )

    scr.scrape(cfg.base_url)
    # log.info(f"Config: {cfg.host}:{cfg.port}")
    # uvicorn.run("isat.scraper.main:app", host=cfg.host, port=cfg.port, reload=True)
