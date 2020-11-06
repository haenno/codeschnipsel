# Aufgabe 2 aus 6. Vorlesung 30.10.2020, Skriptsprachen Python

from tkinter import *
import random
from time import sleep

ROWS = 20
COLS = ROWS
PADDING = 1
BOXSIZE = 25
PAUSE_DURATION = 1.5
GAME_SPEED = 0.2

def game_over():
    global GRID, GAMEOVER
    for i in range(ROWS):
        for j in range(COLS):
            GRID[i][j] = 9
    GAMEOVER = True

def new_target():
    global GRID
   
    need_new_target = True
    while need_new_target: 
        new_target_y = int(random.uniform(0,COLS))
        new_target_x = int(random.uniform(0,ROWS))
        if GRID[new_target_y][new_target_x] == 0:
            GRID[new_target_y][new_target_x] = 2
            need_new_target = False

def set_player(x,y):
    global GRID
    
    for i in range(ROWS):
        for j in range(COLS):
            if GRID[i][j] == 3: 
                GRID[i][j] = 0

    GRID[x][y] = 3

def add_trail():
    global TRAIL, GRID
    TRAIL.insert(0,(int(get_player_pos("x")),int(get_player_pos("y"))))

def move_trail():
    global TRAIL, GRID
    if len(TRAIL)>0:
        delete_trailend_XY = TRAIL.pop()
        GRID[delete_trailend_XY[0]][delete_trailend_XY[1]] = 0
        TRAIL.insert(0,(get_player_pos("x"), get_player_pos("y")))
      

def movement_logic(new_player_x, new_player_y):
    global ROUND_MOVED
    if new_player_x < 0 or new_player_x >= ROWS or new_player_y < 0 or new_player_y >= COLS or GRID[new_player_x][new_player_y] == 1:
        game_over()
    else: 
        if ROUND_MOVED == False:
            if GRID[new_player_x][new_player_y] == 2:
                add_trail()
                new_target()
            else:
                move_trail()  
            set_player(new_player_x,new_player_y)
            ROUND_MOVED = True
            

def get_player_pos(axis):
    for i in range(ROWS):
        for j in range(COLS):
            if GRID[i][j] == 3:
                if axis == "x":
                    return int(i)
                elif axis == "y":
                    return int(j)

def input_up():
    global PLAYER_DIRECTION
    PLAYER_DIRECTION = 1 # 1=north, 2=south, 3=west, 4=east
    movement_logic (get_player_pos("x"), get_player_pos("y")-1)
    #print_field()

def input_left():
    global PLAYER_DIRECTION
    PLAYER_DIRECTION = 3 # 1=north, 2=south, 3=west, 4=east
    movement_logic (get_player_pos("x")-1, get_player_pos("y"))
    #print_field()

def input_right():
    global PLAYER_DIRECTION
    PLAYER_DIRECTION = 4 # 1=north, 2=south, 3=west, 4=east
    movement_logic (get_player_pos("x")+1, get_player_pos("y"))
    #print_field()

def input_down():
    global PLAYER_DIRECTION
    PLAYER_DIRECTION = 2 # 1=north, 2=south, 3=west, 4=east
    movement_logic (get_player_pos("x"), get_player_pos("y")+1)
    #print_field()

def print_field():
    global GRID
    cnv.delete("all")
    for i in range(ROWS):
        x = (i*(BOXSIZE+PADDING))+BOXSIZE
        for j in range(COLS):
            y = (j *(PADDING + BOXSIZE))+BOXSIZE
            x2= x + BOXSIZE
            y2= y + BOXSIZE

            #set marker for trail
            if (i,j) in TRAIL and GRID[i][j] != 3:
                GRID[i][j] = 1

            if GRID[i][j] == 0:
                #empty
                color = "black"
            elif GRID[i][j] == 1:
                #playertrail
                color = "white"
            elif GRID[i][j] == 2:
                #target
                color = "green"
            elif GRID[i][j] == 3:
                #player
                color = "yellow"
            elif GRID[i][j] == 9:
                #gameover
                color = "red"                
            else:
                #fehler
                color = "pink"

            cnv.create_rectangle(x,y,x2,y2,fill=color,outline="")
    cnv.update()
    cnv.update_idletasks()    

def new_field():
    the_new_field =[]
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(0)
        the_new_field.append(row)
    return the_new_field

def move_player():
    try:
        if PLAYER_DIRECTION == 1:
            movement_logic (get_player_pos("x"), get_player_pos("y")-1)
        elif PLAYER_DIRECTION == 2:
            movement_logic (get_player_pos("x"), get_player_pos("y")+1)
        elif PLAYER_DIRECTION == 3:
            movement_logic (get_player_pos("x")-1, get_player_pos("y"))
        else: # must be 4 then
            movement_logic (get_player_pos("x")+1, get_player_pos("y"))
    except:

        pass

gui = Tk()
gui.title("Snake light...")

cnv = Canvas (  gui, 
                width=((ROWS+1)*(BOXSIZE+PADDING))+BOXSIZE-(PADDING*2), 
                height=((COLS+1)*(BOXSIZE+PADDING))+BOXSIZE-(PADDING*2), 
                background="grey")

cnv.pack()

button_up = Button(gui, text="up", width=15, command=input_up)
button_left = Button(gui, text="left", width=15, command=input_left)
button_right = Button(gui, text="right", width=15, command=input_right)
button_down = Button(gui, text="down", width=15, command=input_down)

button_up.pack(side=TOP)
button_left.pack(side=LEFT)
button_right.pack(side=RIGHT)
button_down.pack(side=BOTTOM)


while True:
    # init and prepare game
    TRAIL = list()
    PLAYER_DIRECTION = 4 # 1=north, 2=south, 3=west, 4=east
    ROUND_MOVED = False
    GAMEOVER = False
    GAMERUNNING = True
    GRID = new_field() # create new playfield
    GRID[0][int(round(COLS/2,0))] = 3 # set players dot left and in the middle
    new_target() # set frist target
    print_field() # print first field

    # rest is started by the 4 directional buttons
    #mainloop()
    while GAMERUNNING:
        ROUND_MOVED = False

        cnv.update()
        cnv.update_idletasks()    
        
        if ROUND_MOVED == False: 
            move_player()

        print_field()
        sleep(GAME_SPEED)

        if GAMEOVER == True:
            GAMERUNNING = False
            sleep(PAUSE_DURATION)      
            break
