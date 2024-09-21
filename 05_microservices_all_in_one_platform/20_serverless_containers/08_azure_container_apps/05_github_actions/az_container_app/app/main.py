
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World1", "World2": "Pakistan zindabad 22-9-2024"}
