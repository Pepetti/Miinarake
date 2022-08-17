import sweeperlib as s
import random
import math
from datetime import datetime, timedelta
import time

thisdict = {
  s.MOUSE_LEFT: "left",
  s.MOUSE_MIDDLE: "middle",
  s.MOUSE_RIGHT: "right"
}

state = {
    "field": [],
}
state = {
    "availableCoordinates": [],
}

knownTiles = []

statistics = {
    "outcome": "won",
    "date": None,
    "time": 0,
    "turns": 0,
    "flagAmount": 0,
    "safeTilesLeft": 0,
}


"""
Marks previously unknown connected areas as safe, starting from the given
x, y coordinates.
"""
def floodfill(planet, startX, startY):
    if planet[startY][startX] == 'x':
        return
    xyTuple = [(startY,startX)]
    counter = 0
    while len(xyTuple) > 0:
        [y, x] = xyTuple[0]
        del(xyTuple[0])
        planet[y][x] = '0'
        bombCount = 0
        uusiLista = []
        for row in range(-1, 2):
         for column in range(-1, 2):
            if (x + column) > -1 and (y + row) > -1 and (y + row < len(planet)) and (x + column < len(planet[0])):
                if (planet[row+y][column+x] == 'x'):
                    bombCount += 1
                elif (planet[row+y][column+x] == 'f'):
                    if (tuple([row+y, column+x]) not in state["availableCoordinates"]):
                       bombCount += 1
                elif (planet[row+y][column+x] == ' ' and bombCount == 0):
                    uusiLista.insert(0, tuple([row+y, column+x]))
        if (bombCount in range (1,9)):
            planet[y][x] = str(bombCount)
        else:
            for koordinaatti in uusiLista:
                xyTuple.insert(0, koordinaatti)

"""
Places N mines to a field in random tiles.
"""
def place_mines(field, availableCoordinates, mineAmount):
    statistics["safeTilesLeft"] = len(field) * len(field[0]) - mineAmount
    statistics["flagAmount"] = mineAmount
    count = 0
    while count < mineAmount:
        index = random.randint(0, len(availableCoordinates)-1)
        x = availableCoordinates[index][0]
        y = availableCoordinates[index][1]
        if (field[x][y]) != 'x':
            field[x][y] = 'x'
            state["availableCoordinates"].remove((x,y))
            count = count + 1


"""
A handler function that draws a field represented by a two-dimensional list
into a game window. This function is called whenever the game engine requests
a screen update.
"""
def draw_field():
    s.clear_window()
    s.draw_background()
    s.begin_sprite_draw()
    for j in range(len(state["field"])):
        for i, key in enumerate(state["field"][j]):
            ##if key == 'x' and statistics["outcome"] != "lost":
            ##    key = ' '
            s.prepare_sprite(key, i*40, j*40)
    print(statistics["safeTilesLeft"])
    s.draw_sprites()
    
"""
This function is called when a mouse button is clicked inside the game window.
Prints the position and clicked button of the mouse to the terminal.
"""
def handle_mouse(x, y, mButton, modit):
    if statistics["outcome"] == "lost":
        s.close()
        return
    checkFlagCoordinate = state["field"][int(y/40)][int(x/40)]
    if mButton == s.MOUSE_LEFT:
        if checkFlagCoordinate == 'f':
            return
        else:
            statistics["turns"] += 1
            if (int(y/40), int(x/40)) in state["availableCoordinates"]:
                mButton = thisdict[s.MOUSE_LEFT]
                floodfill(state["field"], int(x/40), int(y/40) )
                s.set_draw_handler(draw_field)
                if not any( (' ') in row for row in state["field"]) and ( not any ( ('f') in row for row in state["field"]) or not any ( ('x') in row for row in state["field"]) ):
                    print("You won the game!")
            else:
                statistics["outcome"] = "lost"
                s.set_draw_handler(draw_field)

    elif mButton == s.MOUSE_RIGHT:
        mButton = thisdict[s.MOUSE_RIGHT]
        if (checkFlagCoordinate == ' '):
            statistics["flagAmount"] -= 1
            state["field"][int(y/40)][int(x/40)] = 'f'
        elif ( checkFlagCoordinate == 'f' and ( int(y/40), int(x/40) ) not in state["availableCoordinates"]):
            statistics["flagAmount"] += 1
            state["field"][int(y/40)][int(x/40)] = 'x'
        elif (checkFlagCoordinate == 'f'):
            statistics["flagAmount"] += 1
            state["field"][int(y/40)][int(x/40)] = ' '
        elif (checkFlagCoordinate == 'x'):
            statistics["flagAmount"] -= 1
            state["field"][int(y/40)][int(x/40)] = 'f'
        print('You have {} flags left'.format(statistics["flagAmount"]))
        s.set_draw_handler(draw_field)

"""
Ask field size from the player
"""
def askFieldSize():
    while True:
        playerInput = input("Give minesweeper game field size (for example 10x10): ")
        if "x" in playerInput and playerInput > "0":
            fieldSize = playerInput.split("x", 1)
            fieldSize[0] = int(fieldSize[0])
            fieldSize[1] = int(fieldSize[1])
            if (fieldSize[0] > 0 and fieldSize[1] > 0 ):
                return fieldSize
            else:
                print("Field size must be greater than 0")
        else:
            print("Input format must be \"number x number\" ")

"""
Ask mine amount from the user 
"""
def askMineAmount(field):
    while True:
        try:
            playerInput = int(input("Give mine amount: "))
            if playerInput < field and playerInput > 0:
                return playerInput
            else:
                print('Mine amount must be bigger than 0 or smaller than given field size')
        except ValueError:
            print('You must enter a number!')

"""
Create field and available coordinates from the given fieldSize 
"""
def createField(fieldSize, mineAmount):
    field = []
    availableCoordinates = []

    for row in range(fieldSize[0]):
            field.append([])
            for col in range(fieldSize[1]):
                field[-1].append(" ")
    state["field"] = field

    for x in range(fieldSize[0]):
            for y in range(fieldSize[1]):
                availableCoordinates.append((x, y))
    state["availableCoordinates"] = availableCoordinates
    place_mines(state["field"], state["availableCoordinates"], mineAmount)

def printMenu():
    while True:
        print("\n1. Start a new game")
        print("2. View statistics")
        print("3. Quit")
        try:
            option = int(input('\nEnter your choice: ')) 
            if option > 0 and option <= 2:
                return option
            elif option == 3:
                print("Thank you for playing!")
                break    
        except ValueError:
            print ("You must enter a number!")
        else:
            print("Enter a number between 1-3")

def textFileHandler(mode):
    if mode == "write":
        statistics["time"] = time.time() - statistics["time"]
        minutes = math.floor(statistics["time"] / 60)
        seconds = math.floor(statistics["time"] % 60)
        with open('statistics.txt', "a") as file:
            file.write("\nGame was played on {}, it lasted {} minutes and {} seconds, there were {} turns and player {} the game".format(statistics["date"], str(minutes), str(seconds), statistics["turns"], statistics["outcome"]))
    if mode == "read":

        try:
            with open('statistics.txt', "r") as file:
                lines = file.readlines()
                for line in lines:
                    print (line)
        except FileNotFoundError:
            print('Statistics file not found')
    

"""
Loads the game graphics, creates a game window, and sets a draw handler
"""
def main():
    while True:
        menuChoice = printMenu()
        if menuChoice == 1:
            statistics["outcome"] = "won"
            statistics["time"] = time.localtime()
            statistics["turns"] = 0

            field = askFieldSize()
            mineAmount = askMineAmount(field[0]*field[1])
            createField(field, mineAmount)
            s.load_sprites(".\sprites")
            s.create_window(len(state["field"][0]) * 40, len(state["field"]) * 40, )
            s.set_draw_handler(draw_field)
            s.set_mouse_handler(handle_mouse)
            statistics["date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            statistics["time"] = time.time()
            s.start()
            textFileHandler("write")
        elif menuChoice == 2:
            textFileHandler("read")
        else:
            break

if __name__ == "__main__":
    main()
