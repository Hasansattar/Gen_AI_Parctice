# fastapi_neon/main.py

from fastapi import FastAPI

app = FastAPI(title="Hello World API", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000/", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])


@app.get("/")
def read_root():
    return {"Hello": "World"}
  
  
@app.get("/{name}")
def read_root(name):
    return {f"Hello {name} " }