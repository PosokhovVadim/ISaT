import base64
from fastapi import FastAPI, File, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import logging

from fastapi.responses import JSONResponse
from isat.imageSearch.search import ImageSearch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

log = logging.getLogger("image-process.log")


@app.post(
    "/im-search",
    summary="find similar images ",
)
async def find_similar_images(
    image: UploadFile = File(...), top_n: int = Query(..., ge=1, le=10)
):
    log.info("Start searching images")
    process = ImageSearch()

    images = await process.image_search(image.file, top_n)
    if len(images) == 0:
        return JSONResponse(status_code=404, content={"error": "images not found"})
    response_data = [
        {"url": img[0], "image": base64.b64encode(img[1]).decode()} for img in images
    ]

    return JSONResponse(content=response_data)
