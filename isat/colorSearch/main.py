import base64
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
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


@app.post(
    "/color-search",
    summary="Search for colors by color. Example: /color-search?r=255&g=0&b=128&color_space=hsv",
)
async def search(
    r: int = Query(..., ge=0, le=255),
    g: int = Query(..., ge=0, le=255),
    b: int = Query(..., ge=0, le=255),
    color_space: str = Query(..., regex="^(lab|hsv)$"),
    top_n: int = Query(..., ge=1, le=10),
):
    log.info(f"Searching for RGB: {r}, {g}, {b} in {color_space} space")

    searcher = ColorSearch()
    images = await searcher.search_process(r, g, b, color_space, top_n)
    if len(images) == 0:
        return JSONResponse(status_code=404, content={"error": "images not found"})
    response_data = [
        {"url": img[0], "image": base64.b64encode(img[1]).decode()} for img in images
    ]

    return JSONResponse(content=response_data)
