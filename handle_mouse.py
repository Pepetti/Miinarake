import sweeperlib as s
import random

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

width, height = 50, 50  # Adjust for width or height of the room
tiles = [" "," ","x"]  # Replace "A", "B", and "C" with your tile instances
knownTiles = []


"""
Marks previously unknown connected areas as safe, starting from the given
x, y coordinates.
"""
def floodfill(planet, startX, startY):
    if planet[startY][startX] == 'x':
        return
    xyTuple = [(startY,startX)]
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
    count = 0
    while count < mineAmount:
        index = random.randint(0, len(availableCoordinates)-1)
        x = availableCoordinates[index][0]
        y = availableCoordinates[index][1]
        if (field[x][y]) != 'x':
            field[x][y] = 'x'
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
            s.prepare_sprite(key, i*40, j*40)
    s.draw_sprites()
    
"""
This function is called when a mouse button is clicked inside the game window.
Prints the position and clicked button of the mouse to the terminal.
"""
def handle_mouse(x, y, mButton, modit):
    if mButton == s.MOUSE_LEFT:
        mButton = thisdict[s.MOUSE_LEFT]
        floodfill(state["field"], int(x/40), int(y/40))
        s.set_draw_handler(draw_field)
    elif mButton == s.MOUSE_RIGHT:
        mButton = thisdict[s.MOUSE_RIGHT]
    elif mButton == s.MOUSE_MIDDLE:
        mButton = thisdict[s.MOUSE_MIDDLE]
    print("The " + str(mButton) + " mouse button was pressed at " + str(int(x/40)) + ", " + str(int(y/40)))

"""
Ask field size from the player
"""
def askFieldSize():
    while True:
        playerInput = input("Give minesweeper game field size (for example 10x10): ")
        if "x" in playerInput:
            fieldSize = playerInput.split("x", 1)
            fieldSize[0] = int(fieldSize[0])
            fieldSize[1] = int(fieldSize[1])
            return fieldSize 

"""
Ask mine amount from the user 
"""
def askMineAmount(field):
    while True:
        playerInput = int(input("Give mine amount: "))
        if playerInput < field and playerInput > 0:
            return playerInput 

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

"""
Loads the game graphics, creates a game window, and sets a draw handler
"""
def main():
    while True:

        field = askFieldSize()
        mineAmount = askMineAmount(field[0]*field[1])
        createField(field, mineAmount)
        s.load_sprites(".\sprites")
        s.create_window(len(state["field"][0]) * 40, len(state["field"]) * 40, )
        s.set_draw_handler(draw_field)
        s.set_mouse_handler(handle_mouse)
        s.start()


if __name__ == "__main__":
    main()
