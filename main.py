from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World 434"}

@app.get("/test")
def read_root():
    return {"Hello": "get test"}

@app.get("/users")
def read_root():
    return {"Hello": "we are users"}

