import os
from fastapi import FastAPI
from isat.scraper.config.config import Config
from isat.scraper import scraper
import logging
import asyncio

app = FastAPI()
log = logging.getLogger("scraper.log")


@app.get("/scrape")
def read_root():
    log.info("Start scraping")
    return {"Service": "1"}


async def run_process():
    log.info("Starting scraper service")

    cfg = Config(os.getenv("CONFIG_PATH"))

    scr = scraper.Scraper(cfg.base_url, cfg.allow_domain)

    await scr.scrape(cfg.base_url)
    # log.info(f"Config: {cfg.host}:{cfg.port}")
    # uvicorn.run("isat.scraper.main:app", host=cfg.host, port=cfg.port, reload=True)


def main():
    asyncio.run(run_process())
