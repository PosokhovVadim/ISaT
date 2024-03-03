import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Service": "1"}


def main():
    print("Starting service")
    uvicorn.run("isat.scraper.main:app", host="0.0.0.0", port=8080, reload=True)
