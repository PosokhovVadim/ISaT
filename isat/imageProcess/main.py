import os
from fastapi import FastAPI
from isat.imageProcess.config.config import Config
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from isat.imageProcess.process import ImageProcess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

log = logging.getLogger("image-process.log")
cfg = Config(os.getenv("CONFIG_PATH"))


@app.post(
    "/im-process",
    summary="process images: 1) removing background 2) count colors 3) count tensors ",
)
async def process_images():
    log.info("Start processing images")
    ip = ImageProcess()
    await ip.image_process()
    return {"message": "Images processed"}


def main():
    log.info(f"Config: {cfg.host}:{cfg.port}")
    uvicorn.run("isat.imageProcess.main:app", host=cfg.host, port=cfg.port, reload=True)
