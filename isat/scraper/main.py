import os
from fastapi import FastAPI
from isat.scraper.config.config import Config
from fastapi.middleware.cors import CORSMiddleware
from isat.scraper.scraper import Scraper
import logging
from isat.scraper.context import ctx
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


log = logging.getLogger("scraper.log")
cfg = Config(os.getenv("CONFIG_PATH"))


@app.get("/scrape/{amount}", summary="Scrape images")
async def scrape_handler(amount: int):
    log.info("Start scraping proccess")
    scr = Scraper(cfg.base_url, cfg.allow_domain, amount)

    await scr.scrape_proccess(cfg.base_url)
    return {"message": f"Scraping of {amount} finished"}


@app.get("/images", summary="Get all images")
async def get_images_handler():
    data = ctx.storage.get_all_images()
    return JSONResponse(content=jsonable_encoder(data))


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down service")
    ctx.storage.close_session()


def main():
    log.info(f"Config: {cfg.host}:{cfg.port}")
    uvicorn.run("isat.scraper.main:app", host=cfg.host, port=cfg.port, reload=True)
