from fastapi import FastAPI
import fastapi
import random
from datetime import datetime, timezone
import json

with open("moves.json", "r") as f:
    moves = json.load(f)

now = datetime.now(timezone.utc)

hour = now.hour
random.seed(hour)

shop = []

for i in range(3):
    shop.append(random.choice(moves))
app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {shop[0]["code"]: shop[0], shop[1]["code"]: shop[1], shop[2]["code"]: shop[2]}