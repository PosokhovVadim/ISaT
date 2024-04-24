import os
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from isat.colorSearch.config.config import Config
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn
from isat.colorSearch.search import ColorSearch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

log = logging.getLogger("color-search.log")
cfg = Config(os.getenv("CONFIG_PATH"))


# do i need to return bytes of image?
@app.post(
    "/color-search",
    summary="Search for colors by color. Example: /color-search?r=255&g=0&b=128&color_space=hsv",
)
async def search(
    r: int = Query(..., ge=0, le=255),
    g: int = Query(..., ge=0, le=255),
    b: int = Query(..., ge=0, le=255),
    color_space: str = Query(..., regex="^(lab|hsv)$"),
    top_n: int = Query(5, ge=1, le=10),
):
    log.info(f"Searching for RGB: {r}, {g}, {b} in {color_space} space")

    searcher = ColorSearch()
    images = await searcher.search_process(r, g, b, color_space, top_n)
    if len(images) == 0:
        return JSONResponse(status_code=404, content={"error": "images not found"})
    return JSONResponse(content=jsonable_encoder(images))


def main():
    log.info(f"Config: {cfg.host}:{cfg.port}")
    uvicorn.run("isat.colorSearch.main:app", host=cfg.host, port=cfg.port, reload=True)
