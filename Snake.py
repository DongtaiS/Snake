# Author: Dongtai Shi
# Date: 28/01/2021
# File Name: Snake.py
# Description: The game snake, avoid running into your tail while picking up as many coins as you can!

import msvcrt
import time
import os
import random

grid = []                                                           #Empty list for grid
snakedirs = []                                                      #Empty list for snake segment directions
snakecoords = []                                                    #Empty list for snake segment coordinates
key_stroke = b''                                                    #Empty bytestring for keystroke input
gameover = False                                                    #Boolean for main loop
gridsize = 0                                                        #Empty variable for size of grid
score = 0                                                           #Integer to count score

print("Welcome to snake! In this game, you control a snake that likes coins [●]. When you pick up a coin, he gets longer!")
print("Use the 'W' key to move up, 'A' key to move left, 'D' key to move right, and 'S' key to move down.")
print("Try to get the snake as long as you can without running into itself, or the walls. Good luck!")
while True:                                                                     #Input loop that repeats until it gets a valid input
    try:
        gridsize = int(input("Please enter the desired size of the grid "))     #Get user input for grid size, must be greater than 3 and less than 50
        if 50 > gridsize > 3:                                                   #If the input is valid, break out of the loop
            break
        else:
            print("Please enter a number between 3 and 50")
    except:                                                                     #If input is not a number, ask again
        print("Please enter a number between 3 and 50")
os.system("mode " + str(max(20, gridsize+1)) + "," + str(max(20, gridsize+1)))  #Changes size of terminal window (minimum size is 20x20)

def printgrid():                        #Prints the whole grid
    for y in range(10):
        print()                         #Print empty lines to clear the last grid
    for y in range(gridsize):
        for x in range (gridsize):
            print(grid[x][y], end='')   #Print string at each grid cell
        print()                         #Print empty line at the end of row

def losegame():             #Called when the player loses
    global gameover         
    gameover = True         #Sets gameover to true which stops main loop

def check_edges(x, y):      #Check if the coordinates are out of bounds, if they are, the player loses
    if (x < 0):
        losegame()
        x = gridsize-1      #Changing value so that out of bounds error doesn't occur, player still loses
    if (x >= gridsize):
        losegame()
        x = 0
    if (y < 0):
        losegame()
        y = gridsize-1
    if (y >= gridsize):
        losegame()
        y = 0
    return [x,y]            #If everything is ok, return the values


def dir_to_coord(x, y, direction):      #Changes a coordinate based on an integer direction value
    if direction == 0:                  #If direction is 0, decrease y-value by 1 (move up)
        return check_edges(x, y-1)
    if direction == 1:                  #If direction is 1, increase x-value by 1 (move right)
        return check_edges(x+1, y)
    if direction == 2:                  #If direction is 2, increase y-value by 1 (move down)
        return check_edges(x, y+1)
    if direction == 3:                  #If direction is 3, decrease x-value by 1 (move left)
        return check_edges(x-1, y)

def spawncoin():                                                #Spawns a coin in the grid
    coordlist = []                                              #Create empty list of coordinates
    for y in range(gridsize):                                           
        for x in range(gridsize):
            if not(grid[x][y] == "■"):                          #For each grid cell, check if there is a snake segment. If there is not, add the coordinate to the list
                coordlist.append([x,y])
    coincoord = coordlist[random.randint(0, len(coordlist)-1)]  #Choose a random coordinate from the list
    grid[coincoord[0]][coincoord[1]] = "●"                      #Change the cell at the coincoord to a coin string in the grid

def movesnake():                                                                                #Moves snake based on direction
    create_segment = False
    for i in range(len(snakecoords)):                                                           #If it is the last (tail) segment, and the snake did not pick up a coin, change the grid square to empty
        if i == len(snakecoords)-1 and not(create_segment):
            grid[snakecoords[i][0]][snakecoords[i][1]] = "□"
            snakecoords[i] = dir_to_coord(snakecoords[i][0], snakecoords[i][1], snakedirs[i])   #Move the segment based on the direction of the one in front in the last move
        else:
            snakecoords[i] = dir_to_coord(snakecoords[i][0], snakecoords[i][1], snakedirs[i])   #Update coordinates based on the direction of segment in front from the last move
            if i == 0: 
                headsquare = grid[snakecoords[i][0]][snakecoords[i][1]]                         #Save the str that the head will move to
                grid[snakecoords[i][0]][snakecoords[i][1]] = "■"                                #Put a snake body part str at the new grid square
                if headsquare == "■":                                                           #If the head tries to move to a snake body part, the player loses
                    losegame()
                elif headsquare == "●":                                                         #If the head tries to move to a coin, the snake gets longer
                    snakecoords.append(snakecoords[len(snakecoords)-1])                         #Add another copy of the coordinates of the tail segment to the list
                    snakedirs.append(snakedirs[len(snakedirs)-1])                               #Add another copy of the direction of the tail segment to the list
                    create_segment = True
                    spawncoin()                                                                 #Increase score by 1.
                    global score
                    score += 1   
    for d in reversed(range(1, len(snakecoords))):                                              #Reversed list to work from the back forward in order to move once each time it is called
        snakedirs[d] = snakedirs[d-1]                                                           #Except for the head segment, update each segment's direction to be the one in front of it

while True:                         #Loop will continue to start new games until player says N to continue
    for x in range(gridsize):
        grid.append([])             #Add a list to grid for each row
        for y in range (gridsize):
            grid[x].append("□")     #Add an empty square for each cell in each column

    grid[gridsize-1][gridsize-3] = "■"              #Change the cell third up from the bottom right to be a snake segment 
    grid[gridsize-1][gridsize-2] = "■"              #Change the cell second up from the bottom right to be a snake segment 
    grid[gridsize-1][gridsize-1] = "■"              #Change the cell in the bottom right to be a snake segment 
    snakedirs.append(0)                             #Add the up direction 3 times for each segment to the snakedirs list, so the snake moves up by default
    snakedirs.append(0)                             
    snakedirs.append(0)
    snakecoords.append([gridsize-1, gridsize-3])    #Add the coordinates of the 3 segments to the snakecoords list
    snakecoords.append([gridsize-1, gridsize-2])
    snakecoords.append([gridsize-1, gridsize-1])

    spawncoin()                                     #Spawn first coin
    printgrid()                                     #Print grid before starting
    print("Start!")
    time.sleep(1)                                   #Pause for 1 second before starting

    while not(gameover):                            #Main loop, while the game is not over, keep repeating
        while msvcrt.kbhit():                       #While the keyboard registers a hit, save the most recent as key_stroke
            key_stroke = msvcrt.getch()
        key_stroke_str = key_stroke.decode("utf-8") #Change the keystroke from byte string to string
        if key_stroke_str == 'w':                   #If the key is w, and the current direction is not up or down, change the direction of the head to up
            if snakedirs[0] % 2 != 0:
                snakedirs[0] = 0
        if key_stroke_str == 'd':                   #If the key is d, and the current direction is not right or left, change the direction of the head to right
            if snakedirs[0] % 2 != 1:
                snakedirs[0] = 1
        if key_stroke_str == 's':                   #If the key is s, and the current direction is not up or down, change the direction of the head to down
            if snakedirs[0] % 2 != 0:
                snakedirs[0] = 2
        if key_stroke_str == 'a':                   #If the key is a, and the current direction is not right or left, change the direction of the head to left
            if snakedirs[0] % 2 != 1:
                snakedirs[0] = 3
        movesnake()                                 #After changing direction of the head, move the snake
        printgrid()                                 #After the snake has been updated, print the new grid
        time.sleep(0.5)                             #Pause for 0.5 seconds

    print("You lose")                           
    print("Your score was: " + str(score))      #Displays player's score
    grid.clear()                                #Clear lists to start again, reset score and keystroke, set gameover back to false
    snakedirs.clear()
    snakecoords.clear()
    score = 0
    key_stroke = b''
    gameover = False
    continue_game = input("Continue? Y/N ")     #Get player input if they would like to continue, if Y, continue, if N, terminate the program
    if continue_game == "N":
        break
    elif continue_game == "Y":
        continue
