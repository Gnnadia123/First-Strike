DATA = {
    "name": "",
    "played" : 0,
    "won" : 0,
    "lost" : 0,
    "gold" : 0,
    "moves" : {
        "charge" : {
            "code": "charge",
            "name": "Charge",
            "desc": "Gain 1 energy.",
            "kill": None,
            "block": None,
            "use": 0,
            "gain": 1,
        },
        "shield": {
            "code": "shield",
            "name": "Shield",
            "desc": "Block your opponent's next attack.",
            "kill": None,
            "block": ["fireball", "sword"],
            "use": 0, 
            "gain": 0,
        },
        "fireball": {
            "code": "fireball",
            "name": "Fireball",
            "desc": "Use 1 energy to hurl a ball of fire at your opponent.",
            "kill": ["charge"],
            "block": ["fireball"],
            "use": 1,
            "gain": 0, 
        },
        "sword": {
            "code": "sword",
            "name": "Sword",
            "desc": "Use 2 energy to land a heavy strike on your opponent.",
            "kill": ["charge", "fireball"],
            "block": ["sword"],
            "use": 2,
            "gain": 0,
        },
        "mountain" :{
            "code": "mountain",
            "name" : "Mountain",
            "desc" : "Use 7 energy to create a formidable mountain",
            "kill" : ["charge", "fireball", "sword", "shield"],
            "block": ["mountain"],
            "use": 7,
            "gain": 0,
        }

    }
}