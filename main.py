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
    return {"shop": {
            "item 1" : shop[0],
            "item 2" : shop[1],
            "item 3" : shop[2]
            }
        }