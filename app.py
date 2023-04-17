import os
import time
from pynput import keyboard
import random

game = []

xSize = 40
ySize = 10

speed = 0.2

item = [3, 1]

snake = [[1, 1], [2, 1]]

direction = "d"
old_direction = "a"

score =-1

def initGame():
    """
    Init empty game array
    """
    game.clear()
    for y in range(ySize):
        row = []
        for x in range(xSize):
            row.append("X")
        game.append(row)


def addItem():
    """
    Add item to game array
    """
    game[item[1]][item[0]] = "I"


def addSnake():
    """
    Add snake to game array
    """
    for piece in snake:
        game[piece[1]][piece[0]] = "S"


def drawGame():
    """
    Draw game in console
    """
    playground = xSize*"M"
    playground += "\n"
    for y in range(len(game)):
        playground += "M"
        for x in range(len(game[y])):
            if game[y][x] == "X":
                playground += " "
            elif game[y][x] == "I":
                playground += "I"
            elif game[y][x] == "S":
                playground += "S"
            elif game[y][x] == "H":
                playground += "H"
        playground += "M\n"
    playground += xSize*"M"

    os.system("cls")
    print(playground)


def on_press(key):
    """
    Callback method on key press (systemwide)
    """
    global direction
    direction = key.char


def moveSnake():
    """
    Move snake depending on key press
    d=right
    s=down
    a=left
    w=up
    """
    global snakes
    global old_direction
    head = snake[-1]
    # move direction test  ==> if direction not allowed then still move direction == old_direction
    move_direction = checkAllowedMoves(direction)
   
    if move_direction == "d" :
        next = [head[0]+1, head[1]]

    elif move_direction == "s":
        next = [head[0], head[1]+1]
  
    elif move_direction == "a":
        next = [head[0]-1, head[1]]

    elif move_direction == "w":
        next = [head[0], head[1]-1]

    # after each move set old_direction in the opposite direction of move_direction
    old_direction= checkDirection(move_direction)

    snake.append(next)
    # Check out of playground
    return next[0] > xSize-1 or next[1] > ySize-1 or next[0] < 0 or next[1] < 0



def checkAllowedMoves(new_direction):
    # Check of the next wanted move is allowed !!
    if old_direction == new_direction:
        return checkDirection(new_direction)
    
    elif new_direction !="a" and  new_direction !="d" and new_direction !="s" and  new_direction !="w":
        return checkDirection(old_direction)
    
    # if move allowd 
    else:
        return new_direction



def checkDirection(check_Fall):
    if check_Fall == "a":
        return "d"
    elif check_Fall =="d":
        return "a"
    elif check_Fall == "w":
        return "s"
    elif check_Fall == "s":
        return "w"
    


def checkItem():
    """
    Check item eaten.
    Extend snake and place new item.
    """
    global snake
    snakeHead = snake[-1]
    if snakeHead[1] == item[1] and snakeHead[0] == item[0]:
        # Item eaten
        placeNewItem()
        
        # nach jedem "Item eaten" wird Scour um 1 vergreoßert
        global score 
        score  +=1
    else:
        snake.pop(0)


def placeNewItem():
    """
    Place new item randomly 
    """
    global item



    randomX = random.randint(0, xSize-1)
    randomY = random.randint(0, ySize-1)

    while game[randomY][randomX] == "S" or game[randomY][randomX] == "H":
        randomX = random.randint(0, xSize-1)
        randomY = random.randint(0, ySize-1)

    item = [randomX, randomY]


def checkBite():
    """
    Check snake array to detect a bite
    """
    bite = False
    snakeHead = snake[-1]
    for piece in snake[:-1]:
        if piece[1] == snakeHead[1] and piece[0] == snakeHead[0]:
            bite = True
            break

    return bite


if __name__ == '__main__':
    # Register listener for keyboard events
    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()

    end = False

    while end == False:
        initGame()

        addItem()
        addSnake()

        drawGame()

        outOfPlayground = moveSnake()
        bite = checkBite()

        if outOfPlayground or bite:
            end = True

        checkItem()
        print("Score :" + str(score))
        time.sleep(speed)

    print("Game over")
