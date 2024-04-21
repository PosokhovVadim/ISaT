import os
from fastapi import FastAPI
from isat.imageProcess.config.config import Config
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

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


def main():
    log.info(f"Config: {cfg.host}:{cfg.port}")
    uvicorn.run("isat.imageProcess.main:app", host=cfg.host, port=cfg.port, reload=True)
