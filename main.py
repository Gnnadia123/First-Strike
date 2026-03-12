from fastapi import FastAPI
import fastapi

app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"idwusyagshus": "World"}