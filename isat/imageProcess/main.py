from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
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


@app.post(
    "/im-process",
    summary="process images: 1) removing background 2) count colors 3) count tensors ",
)
async def process_images():
    log.info("Start processing images")
    process = ImageProcess()
    await process.image_process()
    return {"message": "Images processed"}
