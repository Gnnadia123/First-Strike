import time
import random
import os 
import json
from defaul import DATA

playerData = DATA

def clear(): 
    os.system("clear")

def choose(p):
    while True:
        r = random.choice(list(p.keys()))
        if random.randint(1, 100) <= p[r]:
            return r

def bot(log, boten, en):
    global p
    botlegal = []
    attacks = []
    matrix = []
    probab = {}
    hcount = 0
    lcount = 0
    for move in playerData["moves"].values():
        if move["kill"] != None:
            attacks.append(move["code"])
    if len(log) == 0:
        return "charge"
    else:
        pr1 = log[-1]
        pr2 = log[-2] if len(log) > 1 else None
        pr3 = log[-3] if len(log) > 2 else None
        last3 = [pr1, pr2, pr3]

        for move in playerData["moves"].values():
            if move["use"] <= boten:
                botlegal.append(move["code"])

        probab = {move: 70 for move in botlegal} if botlegal else {"charge": 100}
        if "charge" not in last3 and any(item in attacks for item in last3):
            #if the player has not charged in the last 3 moves and has attacked, most likely they will charge or defend, safe to charge
            probab = {move: 50 for move in botlegal}
            if boten <= 2:
                probab["charge"] = 80
                for item in probab:
                    if item != "charge":
                        probab[item] = 20 / (len(probab) - 1)
            else:
                for item in probab:
                    probab["charge"] = 10
                    probab["shield"] = 10
                    for item in probab:
                        if item != "charge" and item != "shield":
                            probab[item] = 60 / (len(probab) - 1)
        elif "charge" not in last3 and any(item not in attacks for item in last3):
            #if the player has not charged in the last 3 moves and have not attacked, most likely they will charge, best to attack
            if boten >= 1:
                probab = {move: 50 for move in botlegal}
                probab["charge"] = 5
                for item in probab:
                    if item != "charge":
                        probab[item] = 95 / (len(probab) - 1)
            else:
                probab = {move: 50 for move in botlegal}
                probab["charge"] = 90
                for item in probab:
                    if item != "charge":
                        probab[item] = 95 / (len(probab) - 1)
            p = probab
        elif "charge" in last3 and any(item not in attacks for item in last3):
            #if the player has charged in the last 3 moves and have not attacked, most likely they will attack [salvo], best to defend
            probab = {move: 50 for move in botlegal}
            probab["charge"] = 5
            probab["shield"] = 75
            for item in probab:
                if item != "charge":
                    probab[item] = 20 / (len(probab) - 1)
        elif "charge" in last3 and any(item in attacks for item in last3):
            #is the player has charged and attacked in the last 3 moves, and;
            if boten < 1:
                #if the bot has no energy, the player will most likely charge or defend, safe to charge
                probab = {move: 50 for move in botlegal}
                probab["charge"] = 80
                for item in probab:
                    if item != "charge":
                        probab[item] = 20 / (len(probab) - 1)
            elif boten >= 1 and boten <= 3:
                #if the bot has modest energy, the player will most likely charge or defend, safe to attack
                probab = {move: 50 for move in botlegal}
                probab["charge"] = 5
                probab["shield"] = 5
                for item in probab:
                    if item != "charge" and item != "shield":
                        probab[item] = 90 / (len(probab) - 1)
            else:
                #if the bot has high energy, the player will most likely defend, expect a strong defence
                if "mountain" in botlegal:
                    return "mountain"
                elif en >= 2:
                    probab = {move: 50 for move in botlegal}
                    probab["shield"] = 70
                    for item in probab:
                        if item != "shield":
                            probab[item] = 30 / (len(probab) - 1)
                else:
                    probab = {move: 50 for move in botlegal}
                    probab["charge"] = 45
                    probab["shield"] = 15
                    for item in probab:
                        if item != "charge" and item != "shield":
                            probab[item] = 40 / (len(probab) - 1)
            p = probab
    return choose(probab)



def turn():
    boten = 0
    log = []
    botlog = []
    en = 0
    live = True
    botlive = True
    trn = 1
    mov = list(playerData["moves"])
    while live or botlive:
        bmove = bot(log, boten, en)
        botlog.append(bmove)
        boten -= playerData["moves"][bmove]["use"]
        boten += playerData["moves"][bmove]["gain"]
        print(f"Turn {trn}")
        trn += 1
        print("Please choose an action: ")
        print()
        for move in playerData["moves"]:
            print(f"{playerData['moves'][move]['name']} - {playerData['moves'][move]['desc']}")
        print()

        while True:
            try:
                choice = int(input("Your move: ")) - 1   # zero-based index
                if choice < 0 or choice >= len(mov):
                    raise ValueError("Out of range")
                move_cost = playerData["moves"][mov[choice]]["use"]
                if en < move_cost:
                    print("Not enough energy!")
                    continue
                break

            except ValueError:
                print("Invalid selection!")

        clear()
        log.append(playerData['moves'][mov[choice]]["code"])
        en -= move_cost
        en += playerData["moves"][mov[choice]]["gain"]
        
        print(f"You used {playerData['moves'][mov[choice]]['name']}! You have {en} energy.")
        print(f"Bot used {playerData['moves'][bmove]['name']}!")
        if playerData["moves"][mov[choice]]["kill"] != None and bmove in playerData["moves"][mov[choice]]["kill"]:
            print("You win!")
            botlive = False
            return "win"
        elif playerData["moves"][bmove]["kill"] != None and playerData["moves"][mov[choice]]["code"] in playerData["moves"][bmove]["kill"] :
            print("You lose!")
            live = False
            return "lose"
        else:
            continue



def tutorial():
    print("Welcome to First Strike! In this game, you battle against an opponent and try to beat them with different skills and abilities!")
    time.sleep(2)
    clear()
    n = input("What is your name: ")
    playerData["name"] = n
    playerData["gold"] = 100
    with open ("playerData.json", "w+") as f:
        json.dump(playerData, f, indent= 4)

try:
    with open("playerData.json", "r") as f:
        playerData = json.load(f)
except FileNotFoundError:
    tutorial()

result = turn()
if result == "win":
    playerData["won"] += 1
    playerData["gold"] += 10
elif result == "lose":
    playerData["lost"] += 1
    playerData["gold"] += 2
playerData["played"] += 1
with open ("playerData.json", "w+") as f:
    json.dump(playerData, f, indent= 4)