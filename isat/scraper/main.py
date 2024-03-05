import uvicorn
import os
from fastapi import FastAPI
from isat.pkg.logger.logger import Logger
from isat.scraper.config.config import Config

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
    cfg = Config(os.getenv("CONFIG_PATH"))
    log.info(f"Config: {cfg.host}:{cfg.port}")
    uvicorn.run("isat.scraper.main:app", host=cfg.host, port=cfg.port, reload=True)


# todo:
# 1) Implement logger - done
# 2) create cofig  - sooo, why??? - done
# 3) Implement crowler (async ???)
# 4) Implement scraper (where contain img, check async impl.) thats all?)
