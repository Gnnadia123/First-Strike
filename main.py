from fastapi import FastAPI
import fastapi
import random
from datetime import datetime, timezone
import json

with open('/Users/aidanng/Desktop/Desktop Items/Code/First Strike/First Strike/moves.json', "r") as f:
    moves_data = json.load(f)

moves = list(moves_data.values())

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
            "item 1" : shop[0]["code"],
            "item 2" : shop[1]["code"],
            "item 3" : shop[2]["code"]
            }
        }