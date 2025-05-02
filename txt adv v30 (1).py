import datetime
import time
import sys

try:
    colour = sys.stdout.shell  # This works in IDLE
except AttributeError:
    def dummy_write(text, tag=None):
        print(text)
    class DummyShell:
        write = dummy_write
    colour = DummyShell()


def game():
    tries = 0
    back = 0
    looking = 0
    mid = 0
    name = input("\nWhat is your name? ")

    colour.write(f"""
 _______                                            
(  ___  )                    _                     
| |___| |____  _____  ____ _| |_ _   _  ____ _____ 
|  ___  |  _ \| ___ |/ ___|_   _) | | |/ ___) ___ |
| |   | | |_| | ____| |     | |_| |_| | |   | ____|
|_|   |_|  __/|_____)_|      \__)____/|_|   |_____)
        |_|                                        \n""", "STRING")

    colour.write("Your workplace has been locked down. There's a killer inside. You and Aidyn must survive.\n", "console")
    colour.write(f"Hello {name}. You must move to a safe place as soon as possible.\n", "console")

    def kill():
        colour.write("You died.\n", "COMMENT")
        quit()

    def corridor():
        colour.write("You see a long corridor stretching ahead...\n", "console")

    def middle():
        colour.write("Storage room. It smells like bleach and something else... You find a swiss knife.\n", "console")

    def middle2():
        colour.write("You're in the common room. Aidyn is nervous.\n", "console")
        hideroom1()

    def look():
        colour.write("Aidyn: Hurry up before you're pulverized!\n", "ERROR")

    def look2():
        colour.write(f"Aidyn: Please, stop looking {name}, we're going to die.\n", "stdout")

    def look3():
        colour.write("Your heart pounds... Something is wrong with Aidyn.\n", "console")
        colour.write(f"Aidyn: It's been fun, {name}, but goodbye.\n", "stderr")
        endall()

    def backward():
        colour.write("???: Moving back won't save you.\n", "ERROR")
        again()

    def endall():
        end()
        end2()

    def end():
        colour.write(f"{name}, you've ruined everything.\n", "COMMENT")
        again()

    def end2():
        colour.write("Aidyn betrays you.\n", "ERROR")
        kill()
        again()

    def hideroom1():
        colour.write("You hide. Someone enters. Silence follows...\n", "console")

    def again():
        retry = input("/aperture.exe has crashed. Restart? (yes/no): ").lower()
        if retry in ["yes", "y", "1"]:
            game()
        elif retry in ["no", "n", "2"]:
            quit()
        else:
            print("Type 'yes' or 'no'.")
            again()

    def happyend():
        colour.write("You reach the reception. Aidyn grins... suspiciously.\n", "console")
        die = input("Do you want to kill Aidyn? (yes/no): ").lower()

        if die.startswith("y"):
            colour.write("You stab Aidyn. You win.\n", "BUILTIN")
            kds = input("Kill or show mercy to the creator? (mercy/kill): ").lower()
            if kds == "kill":
                colour.write("The creator is dead.\n", "BUILTIN")
                again()
            elif kds == "mercy":
                colour.write(f"You let me live... Thank you, {name}. You win.\n", "KEYWORD")
                again()
            else:
                print("You must choose.")
                happyend()
        elif die == "no":
            colour.write("Aidyn kills you.\n", "COMMENT")
            end2()
        else:
            print("Choose one.")
            happyend()

    room = "start"

    while room == "start":
        looking += 1
        print("\nActions available: forward, middle, backward, look, end")
        action = input("> ").lower()

        if action == "forward":
            tries += 1
            if tries == 1:
                middle2()
            elif tries == 2:
                middle()
            elif tries >= 3:
                endall()

        elif action == "backward":
            back += 1
            if back == 1:
                backward()

        elif action == "middle":
            mid += 1
            if mid == 1:
                middle()
            elif mid == 2:
                middle2()
            elif mid >= 3:
                happyend()

        elif action == "look":
            if looking == 1:
                look()
            elif looking == 2:
                look2()
            elif looking >= 3:
                look3()

        elif action == "end":
            end()

        else:
            print("Try again.")

# Start the game
game()
