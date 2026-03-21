from fastapi import FastAPI
import random
from datetime import datetime, timezone
import json
import os

app = FastAPI()

# Load moves safely using relative path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVES_PATH = os.path.join(BASE_DIR, "moves.json")

with open(MOVES_PATH, "r") as f:
    moves_data = json.load(f)

moves = list(moves_data.values())


def generate_shop():
    now = datetime.now(timezone.utc)
    hour = now.hour

    random.seed(hour)  # same shop for the same hour

    shop = [random.choice(moves) for _ in range(3)]
    return shop


@app.get("/")
def read_root():
    return {
        "shop": "working"
    }