# main.py

from fastapi import FastAPI, Depends




app = FastAPI( title="Hello World API with DB", 
    version="0.0.1",
    servers=[
        {
            "url": "http://0.0.0.0.:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])



@app.get("/")
def read_root():
    return {"Hello": "World"}

