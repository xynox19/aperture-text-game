import sys
import time

#Colours
try:
    shell = sys.stdout.shell  # only exists in IDLE
    def c(text, tag="console"):
        shell.write(text + "\n", tag)
    IDLE = True
except AttributeError:
    def c(text, tag=None):
        print(text)
    IDLE = False

# IDLE colour tags used:
#   "console"  → default white/black
#   "STRING"   → green  (locations, scene descriptions)
#   "KEYWORD"  → orange (important items, choices)
#   "COMMENT"  → red    (death, danger)
#   "ERROR"    → bright red (killer dialogue, threats)
#   "stdout"   → blue   (Aidyn dialogue)
#   "BUILTIN"  → purple (victory)
#   "stderr"   → dark red (betrayal)

#Metrics/helpers
def pause(secs=0.6):
    time.sleep(secs)

def blank():
    c("")

def divider():
    c("─" * 52, "console")

def title_card():
    c(f"""
 _______                                            
(  ___  )                    _                     
| |___| |____  _____  ____ _| |_ _   _  ____ _____ 
|  ___  |  _ \| ___ |/ ___|_   _) | | |/ ___) ___ |
| |   | | |_| | ____| |     | |_| |_| | |   | ____|
|_|   |_|  __/|_____)_|      \__)____/|_|   |_____)
        |_|                                        \n""", "STRING")
    c("  A TEXT ADVENTURE", "KEYWORD")
    blank()

def ask(prompt_text):
    return input(prompt_text).strip().lower()

def slow_print(lines, tag="console", delay=0.55):
    for line in lines:
        c(line, tag)
        pause(delay)

#Game
def game():
    title_card()

    c("Your workplace has been locked down.", "console")
    c("A killer is somewhere inside.", "console")
    c("You and your colleague Aidyn must survive.", "console")
    blank()

    name = input("What is your name? ").strip()
    if not name:
        name = "Stranger"

    blank()
    divider()
    c(f"Hello, {name}.", "KEYWORD")
    c("Move to safety as quickly as you can.", "console")
    divider()
    blank()

    #State of player
    inventory = []
    moves     = 0
    flags = {
        "looked":        0,
        "went_back":     0,
        "in_storage":    False,
        "knife_taken":   False,
        "in_common":     False,
        "common_visits": 0,
        "aidyn_trust":   3,   # decrements with suspicion
    }

    def stat_line():
        inv = ", ".join(inventory) if inventory else "nothing"
        c(f"  Moves: {moves}  |  Inventory: {inv}", "console")

    #Death message
    def die(msg):
        blank()
        c(msg, "COMMENT")
        pause(0.8)
        c("YOU HAVE DIED.", "COMMENT")
        blank()
        restart()
        
    #Restart
    def restart():
        again = ask("Restart? (yes / no): ")
        if again in ("yes", "y"):
            blank()
            game()
        elif again in ("no", "n"):
            c("Goodbye.", "console")
            sys.exit()
        else:
            c("Please type yes or no.", "console")
            restart()

    #Rooms
    def room_corridor():
        c("CORRIDOR A", "STRING")
        c("A long corridor stretches ahead of you. Fluorescent lights flicker.", "console")
        c("There is a heavy door to your left marked STORAGE.", "console")
        c("Aidyn stands close behind you, breathing fast.", "console")

    def room_storage():
        flags["in_storage"] = True
        c("STORAGE ROOM", "STRING")
        c("The smell of bleach hits you hard. Wire shelves line the walls.", "console")
        if not flags["knife_taken"]:
            c("Something glints on the lower shelf — a swiss army knife.", "KEYWORD")
        else:
            c("The shelf where the knife was is empty.", "console")

    def room_common():
        flags["in_common"] = True
        flags["common_visits"] += 1
        c("COMMON ROOM", "STRING")
        if flags["common_visits"] == 1:
            c("Vending machines, cheap chairs, a kitchenette.", "console")
            c("Aidyn is here, pacing by the window.", "console")
        else:
            c("You're back in the common room. Aidyn watches you carefully.", "console")
            if flags["aidyn_trust"] <= 1:
                c("Something in Aidyn's eyes has changed.", "stderr")

    def room_reception():
        c("RECEPTION", "STRING")
        c("The main lobby. Emergency lighting. The front doors are chained shut.", "console")
        c(f"Aidyn grins at you, {name}. It is not a comforting grin.", "stderr")

    #Dialogues
    def aidyn_says(line):
        c(f"Aidyn: {line}", "stdout")

    def aidyn_threat(line):
        c(f"Aidyn: {line}", "ERROR")

    #Actions
    def do_look():
        nonlocal moves
        flags["looked"] += 1
        moves += 1
        if flags["looked"] == 1:
            aidyn_says("Hurry up before you're pulverized!")
        elif flags["looked"] == 2:
            aidyn_says(f"Please, stop looking around, {name}. We're going to die.")
            flags["aidyn_trust"] -= 1
        elif flags["looked"] >= 3:
            c("Your heart pounds. Something is very wrong with Aidyn.", "console")
            pause(0.8)
            aidyn_threat(f"It's been fun, {name} — but goodbye.")
            pause(0.6)
            die(f"Aidyn was the killer all along.")

    def do_examine(target):
        nonlocal moves
        moves += 1
        if target in ("knife", "swiss", "blade") and flags["in_storage"]:
            if flags["knife_taken"]:
                c("You already have the knife.", "console")
            else:
                c("A red-handled swiss army knife. Still sharp.", "KEYWORD")
        elif target in ("door", "doors"):
            c("Heavy, sealed. The chains on the front doors look new.", "console")
        elif target in ("aidyn",):
            flags["aidyn_trust"] -= 1
            if flags["aidyn_trust"] >= 2:
                aidyn_says("What are you staring at? Keep moving.")
            else:
                aidyn_threat("Stop looking at me like that.")
        elif target in ("shelf", "shelves"):
            c("Wire shelves. Cleaning products. A dusty binder labelled MAINTENANCE.", "console")
        else:
            c("You don't see anything notable there.", "console")

    def do_take(target):
        nonlocal moves
        moves += 1
        if target in ("knife", "swiss", "blade", "swiss army knife"):
            if not flags["in_storage"]:
                c("There's no knife here.", "console")
            elif flags["knife_taken"]:
                c("You already have it.", "console")
            else:
                flags["knife_taken"] = True
                inventory.append("swiss army knife")
                c("You take the swiss army knife.", "KEYWORD")
                aidyn_says("Good thinking. Let's keep moving.")
        else:
            c(f"You can't take that.", "console")

    def do_talk():
        nonlocal moves
        moves += 1
        flags["aidyn_trust"] -= 1
        if flags["aidyn_trust"] >= 2:
            aidyn_says("There's no time to talk. We need to get out.")
        elif flags["aidyn_trust"] == 1:
            aidyn_says("Stop wasting time, or I'll leave you behind.")
        else:
            aidyn_threat(f"I warned you, {name}.")
            die("Aidyn turns on you. You were too slow to react.")

    def do_inventory():
        if inventory:
            c("You are carrying:", "KEYWORD")
            for item in inventory:
                c(f"  · {item}", "KEYWORD")
        else:
            c("You are carrying nothing.", "console")

    #Endings
    def ending_reception():
        blank()
        room_reception()
        blank()
        pause(0.8)
        c("Aidyn steps between you and the door.", "console")
        blank()

        if flags["knife_taken"]:
            c("Your hand tightens around the knife in your pocket.", "KEYWORD")
            choice = ask("Do you confront Aidyn? (yes / no): ")
            if choice in ("yes", "y", "confront"):
                blank()
                c("You draw the knife.", "KEYWORD")
                pause(0.6)
                c("Aidyn hesitates. Just long enough.", "console")
                pause(0.8)
                blank()
                c("You survive.", "BUILTIN")
                c(f"Well played, {name}.", "BUILTIN")
                blank()
                restart()
            else:
                die("You hesitate. Aidyn does not.")
        else:
            c("You have nothing to defend yourself with.", "COMMENT")
            pause(0.7)
            die("Aidyn was the killer. You never stood a chance.")

    def ending_flee_back():
        nonlocal moves
        flags["went_back"] += 1
        moves += 1
        if flags["went_back"] == 1:
            c("A voice behind you, low and calm:", "console")
            c("???: Moving backwards won't help you.", "ERROR")
            blank()
            c("You are back at the start of the corridor.", "console")
            room_corridor()
        else:
            die("You ran — and ran directly into the killer.")

    #Main
    location = "corridor"
    room_corridor()
    blank()

    while True:
        stat_line()
        blank()
        raw = ask("> ")
        blank()
        tokens = raw.strip().lower().split()
        if not tokens:
            c("Pardon?", "console")
            continue

        verb = tokens[0]
        obj  = " ".join(tokens[1:]) if len(tokens) > 1 else ""

        #Quit/Help menu
        if verb in ("quit", "exit", "q"):
            c("Goodbye.", "console")
            sys.exit()

        if verb == "help":
            c("COMMANDS:", "KEYWORD")
            c("  go [forward / back / middle]", "console")
            c("  look                          — examine your surroundings", "console")
            c("  examine [thing]               — look closely at something", "console")
            c("  take [item]                   — pick something up", "console")
            c("  talk to aidyn                 — speak with Aidyn", "console")
            c("  inventory                     — check what you're carrying", "console")
            c("  quit                          — end the game", "console")
            continue

        #Check inventory
        if verb in ("inventory", "i", "inv"):
            do_inventory()
            continue

        #Look around
        if verb == "look" and not obj:
            do_look()
            continue

        #Examine
        if verb in ("examine", "x", "inspect", "look") and obj:
            do_examine(obj)
            continue

        #Take
        if verb in ("take", "get", "grab", "pick"):
            item = obj.replace("up ", "").strip()
            do_take(item)
            continue

        #Talk options
        if verb in ("talk", "speak", "say", "ask") and "aidyn" in obj:
            do_talk()
            continue

        #Movement
        direction = ""
        if verb in ("go", "move", "walk", "run", "head"):
            direction = obj
        elif verb in ("forward", "north", "ahead", "f"):
            direction = "forward"
        elif verb in ("back", "backward", "south", "b", "return", "retreat"):
            direction = "back"
        elif verb in ("middle", "left", "storage", "side"):
            direction = "middle"

        if direction in ("forward", "north", "ahead", "f", "front"):
            if location == "corridor":
                location = "common"
                room_common()
            elif location == "storage":
                location = "common"
                room_common()
            elif location == "common":
                location = "reception"
                ending_reception()
                break
            else:
                c("You can't go that way.", "console")

        elif direction in ("back", "backward", "south", "b", "return", "retreat"):
            if location == "corridor":
                ending_flee_back()
            elif location == "storage":
                location = "corridor"
                room_corridor()
            elif location == "common":
                location = "corridor"
                room_corridor()
            else:
                c("There's nowhere to go back to.", "console")

        elif direction in ("middle", "left", "storage", "side"):
            if location == "corridor":
                location = "storage"
                room_storage()
            elif location == "storage":
                c("You're already in the storage room.", "console")
            else:
                c("There's no storage room accessible from here.", "console")

        elif direction:
            c(f"You can't go {direction} from here.", "console")

        else:
            c("I don't understand that. Try HELP for a list of commands.", "console")

        blank()
        moves += 1


#Entry point
if __name__ == "__main__":
    game()
