import time
import random
import os 
import json
from defaul import DATA
import requests
from datetime import datetime, timezone

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'playerData.json')


legal = ["charge", "shield", "fireball", "sword", "mountain"]



def clear(): 
    os.system("clear")

def choose(p):
    while True:
        r = random.choice(list(p.keys()))
        if random.randint(1, 100) <= p[r]:
            return r

def bot(log, boten):
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
        elif "charge" in last3 and any(item in attacks for item in last3):
            #the player will most likely not charge, but will attack or defend
            probab = {move: 50 for move in botlegal}
            probab["charge"] = 5
            for item in probab:
                if item != "charge":
                    probab[item] = 95 / (len(probab) - 1)
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
        bmove = bot(log, boten)
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
    playerData = DATA
    print("Welcome to First Strike! In this game, you battle against an opponent and try to beat them with different skills and abilities!")
    time.sleep(2)
    clear()
    n = input("What is your name: ")
    playerData["name"] = n
    playerData["gold"] = 100
    with open (data_path, "w+") as f:
        json.dump(playerData, f, indent= 4)


def shop(moves):
    c = ""
    now = datetime.now(timezone.utc)
    seed = int(now.strftime("%Y%m%d%H"))
    rng = random.Random(seed)
    owned_names = {m["name"] for m in playerData["moves"].values()}
    valid_moves = [
        m for m in moves.values()
        if m["legal"] == True and m["name"] not in owned_names
    ]


    if not valid_moves:
        print("The shop is empty… wait for future updates!")
        return
    
    shop_size = min(3, len(valid_moves))
    s = rng.sample(valid_moves, shop_size)

    while c != "q":
        print(f"Shop: sequence {now.hour + 1} of {now.day}/{now.month}/{now.year}")
        for i in range(len(s)):
            print(f"{i+1}. {s[i]['name']} - {s[i]['price']} gold")
        
        print()
        c = input(f"Enter your choice (1-{len(s)}), q to exit: ").lower()
        
        if c == "q":
            break
        
        try:
            choice = int(c) - 1
            item = s[choice]
            print(f"{item['name']}:")
            print(item["desc"])
            print(f"Price: {item['price']}")
            print()
            print(f"Your balance: {playerData['gold']}")
            if playerData["gold"] < item["price"]:
                print("Insufficient balance!")
                time.sleep(2)
                clear()
                continue
            buy = input("Would you like to purchase this item? [Y/N] ").upper()
            if buy == "Y":
                new_move = item.copy()
                new_move["inuse"] = False
                playerData["moves"][new_move["name"]] = new_move
                playerData["gold"] -= item["price"]
                s.pop(choice)
                print(f"Success! You now have {playerData['gold']} gold left!")
                time.sleep(2)
                clear()
                if not s:
                    print("The shop is sold out. Come back later.")
                    break
            else:
                clear()
        except (ValueError, IndexError):
            print("Invalid selection!!")
            time.sleep(2)
            clear()


def menu(playerData):
    try:
        BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
        MOVES_PATH = os.path.join(BASE_DIR2, "moves.json")
        with open (MOVES_PATH, "r") as m:
            moves = json.load(m)
    except:
        print("Missing files!!")
        os._exit(0)
    while True:
        clear()
        print("-- First Strike --")
        print("1. Battle")
        print("2. Deck")
        print("3. Shop")
        print("4. Stats")
        print("5. Exit")
        print(" ---==========--- ")
        print()
        choice = input("Select an option: ")
        clear()
        if choice == "1": 
            result = turn()
            if result == "win":
                g = random.randint(10,20)
                playerData["won"] += 1
                playerData["played"] += 1
                playerData["gold"] += g
                print(f"You won! You earned {g} gold!")
                print(f"Your current balance is {playerData["gold"]}")
            elif result == "lose":
                g = random.randint(2,5)
                playerData["lost"] += 1
                playerData["played"] += 1
                playerData["gold"] += g
                print("You lost! Better luck next time!")
            time.sleep(2)
            clear()
        elif choice == "2":
            print("Deck Management!")
            print("Each deck can only consist of 2 misc, 2 attacks, and 1 attack+")
            mov = list(playerData["moves"])
            for i in range(len(mov)):
                move = playerData["moves"][mov[i]]
                if move["inuse"]:
                    print(f"{i+1}. {move['name']} - {move['desc']}")
            c = input("Choose a move to view or modify (1-{}), q to quit: ".format(len(mov))).lower()
            if c == "q":
                clear()
            else:
                try:
                    c_index = int(c) - 1
                    if 0 <= c_index < len(mov):
                        selected_move_key = mov[c_index]
                        selected_move = playerData["moves"][selected_move_key]
                        print(f"\n{selected_move['name']} - {selected_move['desc']}")
                        print(f"Slot: {c_index + 1}")
                        print(f"Type: {selected_move['type']}")
                        print(f"Use: {selected_move['use']}")
                        print(f"Gain: {selected_move['gain']}")
                        print(f"Kill: {selected_move['kill']}")
                        print(f"Block: {selected_move['block']}")
                        print(f"In use: {selected_move['inuse']}\n")
                        pos = []
                        for i, key in enumerate(mov):
                            move = playerData["moves"][key]
                            if (
                                move["type"] == selected_move["type"]
                                and not move["inuse"]
                                and move["code"] not in legal
                            ):
                                pos.append(key)

                        if pos:
                            print("Available moves to swap with:")
                            for i, key in enumerate(pos):
                                move = playerData["moves"][key]
                                print(f"{i+1}. {move['name']} - {move['desc']}")

                            swap = input("Choose a move to swap with or press enter to go back: ")
                            if swap:
                                swap_index = int(swap) - 1
                                if 0 <= swap_index < len(pos):
                                    swap_key = pos[swap_index]

                                    # Turn off all moves of this type
                                    for key in playerData["moves"]:
                                        if playerData["moves"][key]["type"] == selected_move["type"]:
                                            playerData["moves"][key]["inuse"] = False

                                    # Activate the chosen move
                                    playerData["moves"][swap_key]["inuse"] = True

                                    # Optionally, update the order in mov
                                    index_to_swap = mov.index(swap_key)
                                    mov[c_index], mov[index_to_swap] = mov[index_to_swap], mov[c_index]

                                    print(f"Move swapped! {playerData['moves'][swap_key]['name']} is now active.")
                                    with open(data_path, "w") as f:
                                        json.dump(playerData, f, indent=4)
                                    time.sleep(2)
                                else:
                                    print("Invalid selection!")
                                    time.sleep(2)
                            else:
                                print("No swap made.")
                                time.sleep(1)
                        else:
                            print("No available moves to swap with!")
                            time.sleep(2)
                            clear()
                    else:
                        print("Invalid move number!")
                        time.sleep(2)
                        clear()
                except (ValueError, IndexError):
                    print("Invalid selection!")
                    time.sleep(2)
                    clear()
        elif choice == "3":
            #shop(moves)
            print("Shop coming soon!")
        elif choice == "4":
            clear()
            print("Your Stats")
            print()
            print(f"Name: {playerData['name']}")
            print(f"Games Played: {playerData['played']}")
            print(f"Games Won: {playerData['won']}")
            print(f"Games Lost: {playerData['lost']}")
            try:
                print(f"Win Rate: {playerData['won'] / playerData['played'] * 100:.2f}%")
            except:
                print(f"Win Rate: 0.00%")
            print()
            print(f"Gold: {playerData['gold']}")
            print()
            input("Press enter to continue...")
        elif choice == "5":
            with open(data_path, "w") as f:
                json.dump(playerData, f, indent=4)
            print("Goodbye!")
            time.sleep(1)
            break
        else:
            print("Invalid selection!")
            time.sleep(2)
            clear()

try:
    with open(data_path, "r") as f:
        playerData = json.load(f)
except:
    tutorial()

menu(playerData)