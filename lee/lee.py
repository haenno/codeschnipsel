from tkinter import *
import random
from time import sleep

GAME_SPEED = 0.0001
PADDING = 1
BOXSIZE = 30


START_POS = (14,17)
TARGET_POS = (36,7)
WALLS = [(4,1),(6,1),(7,1),(8,1),(9,1),(11,1),(36,1),(37,1),(38,1),(4,2),(9,2),(11,2),(13,2),(14,2),(15,2),(16,2),(17,2),(18,2),(19,2),(20,2),(21,2),(22,2),(23,2),(24,2),(25,2),(26,2),(27,2),(28,2),(29,2),(30,2),(31,2),(32,2),(33,2),(34,2),(37,2),(4,3),(5,3),(6,3),(7,3),(9,3),(11,3),(15,3),(25,3),(34,3),(36,3),(37,3),(38,3),(4,4),(9,4),(11,4),(13,4),(15,4),(17,4),(18,4),(19,4),(20,4),(21,4),(23,4),(24,4),(25,4),(34,4),(1,5),(2,5),(3,5),(4,5),(6,5),(7,5),(8,5),(9,5),(13,5),(17,5),(25,5),(34,5),(35,5),(36,5),(37,5),(4,6),(9,6),(11,6),(13,6),(15,6),(17,6),(19,6),(20,6),(21,6),(22,6),(23,6),(24,6),(25,6),(34,6),(4,7),(9,7),(11,7),(13,7),(15,7),(17,7),(34,7),(3,8),(4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),(12,8),(13,8),(14,8),(15,8),(16,8),(17,8),(18,8),(19,8),(20,8),(21,8),(22,8),(23,8),(24,8),(25,8),(26,8),(27,8),(28,8),(29,8),(30,8),(34,8),(35,8),(36,8),(37,8),(38,8),(39,8),(22,9),(39,9),(0,10),(1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(16,10),(17,10),(18,10),(19,10),(20,10),(22,10),(23,10),(24,10),(25,10),(26,10),(27,10),(28,10),(29,10),(30,10),(31,10),(32,10),(33,10),(34,10),(35,10),(36,10),(39,10),(20,11),(22,11),(24,11),(28,11),(32,11),(1,12),(2,12),(3,12),(4,12),(5,12),(6,12),(7,12),(8,12),(9,12),(10,12),(11,12),(12,12),(13,12),(14,12),(15,12),(16,12),(17,12),(18,12),(19,12),(20,12),(24,12),(26,12),(28,12),(30,12),(32,12),(35,12),(36,12),(37,12),(38,12),(20,13),(22,13),(24,13),(26,13),(28,13),(30,13),(32,13),(36,13),(37,13),(38,13),(0,14),(1,14),(2,14),(3,14),(4,14),(5,14),(6,14),(7,14),(8,14),(9,14),(10,14),(11,14),(12,14),(13,14),(14,14),(15,14),(16,14),(17,14),(18,14),(20,14),(22,14),(24,14),(26,14),(28,14),(30,14),(32,14),(37,14),(38,14),(20,15),(22,15),(24,15),(26,15),(28,15),(30,15),(32,15),(33,15),(38,15),(39,15),(1,16),(2,16),(3,16),(4,16),(5,16),(6,16),(7,16),(8,16),(9,16),(10,16),(11,16),(12,16),(13,16),(14,16),(15,16),(16,16),(17,16),(18,16),(19,16),(20,16),(22,16),(24,16),(26,16),(28,16),(30,16),(33,16),(34,16),(39,16),(22,17),(24,17),(26,17),(28,17),(30,17),(34,17),(35,17),(1,18),(2,18),(3,18),(4,18),(6,18),(7,18),(9,18),(10,18),(18,18),(19,18),(20,18),(22,18),(24,18),(26,18),(28,18),(30,18),(35,18),(36,18),(22,19),(26,19),(30,19)]
X_COLS = 40
Y_ROWS = 20
PAUSE_DURATION = 2.5


def print_field():
    global GRID
    cnv.delete("all")
    for i in range(X_COLS):
        x = (i*(BOXSIZE+PADDING))+BOXSIZE
        for j in range(Y_ROWS):
            y = (j *(PADDING + BOXSIZE))+BOXSIZE
            x2= x + BOXSIZE
            y2= y + BOXSIZE

            if GRID[i][j] == 0:
                #empty
                color = "white"
            elif GRID[i][j] == 1:
                #walls
                color = "black"
            elif GRID[i][j] == 6:
                #backtrack
                color = "blue"  
            elif GRID[i][j] == 7:
                #start
                color = "green"   
            elif GRID[i][j] == 8:
                #target
                color = "yellow"   
            elif GRID[i][j] == 9:
                #gameover
                color = "red"     
            elif GRID[i][j] == 30:
                #done search
                color = "white"
            elif GRID[i][j] == 40:
                #last search
                color = "grey"      
                GRID[i][j] = 30
            elif GRID[i][j] == 50:
                #current search
                color = "lime"  
                GRID[i][j] = 40           
            else:
                #fehler
                color = "pink"

            cnv.create_rectangle(x,y,x2,y2,fill=color,outline="")
            if FIELDVALUES[i][j] == 0:
                field_text = ""
            else:
                field_text = str(FIELDVALUES[i][j])
            cnv.create_text((x+(BOXSIZE/2),y+(BOXSIZE/2)), text=field_text)
    cnv.update()
    cnv.update_idletasks()
    sleep(GAME_SPEED)       

def new_field():
    the_new_field =[]
    for i in range(X_COLS):
        row = []
        for j in range(Y_ROWS):
            row.append(0)
        the_new_field.append(row)
    return the_new_field

# SETUP WINDOW
gui = Tk()
gui.title("Lee Maze...")
cnv = Canvas (  gui, 
                width=((X_COLS+1)*(BOXSIZE+PADDING))+BOXSIZE-(PADDING*2), 
                height=((Y_ROWS+1)*(BOXSIZE+PADDING))+BOXSIZE-(PADDING*2), 
                background="grey")
cnv.pack()

def end_game(msg, type):
    global GRID, GAMERUNNING, weitersuchen
    weitersuchen = False
    GAMERUNNING = False          
    print_field()
    print(msg)
    sleep(PAUSE_DURATION)  

def pos_pruefen(wert,x,y):
    global FIELDVALUES, weitersuchen, arbeitsvorrat

    N=y+1
    E=x+1
    S=y-1
    W=x-1

    if ((N >= 0) & (N <= Y_ROWS-1)):
        if FIELDVALUES[x][N] == 0:
            FIELDVALUES[x][N] = wert
            GRID[x][N]=50
            arbeitsvorrat.append((wert,x,N))

    if ((E <= X_COLS-1) & (E >= 0)):
        if FIELDVALUES[E][y] == 0:
            FIELDVALUES[E][y] = wert
            GRID[E][y]=50
            arbeitsvorrat.append((wert,E,y))

    if ((S >= 0 ) & ( S <= Y_ROWS-1)):
        if FIELDVALUES[x][S] == 0:
            FIELDVALUES[x][S] = wert
            GRID[x][S]=50
            arbeitsvorrat.append((wert,x,S))

    if ((W <= X_COLS-1 ) & ( W >= 0)):
        if FIELDVALUES[W][y] == 0:
            FIELDVALUES[W][y] = wert
            GRID[W][y]=50
            arbeitsvorrat.append((wert,W,y))      

while True:
    print("Neue Runde...")
    # SETUP GAME
    GAMERUNNING = True

    # CREATE NEW GRID FOR THE GAME
    GRID = new_field() 
    
    # CREATE HELPER GRID FOR LEE VALUES
    FIELDVALUES = new_field()

    for i in range(X_COLS):
        for j in range(Y_ROWS):
            if (i,j) in WALLS and GRID[i][j] != 3:
                GRID[i][j] = 1
                FIELDVALUES[i][j] = ""

    # SET START AND TARGET
    FIELDVALUES[START_POS[0]][START_POS[1]] = "S"
    GRID[START_POS[0]][START_POS[1]] = 7 

    FIELDVALUES[TARGET_POS[0]][TARGET_POS[1]] = 0
    GRID[TARGET_POS[0]][TARGET_POS[1]] = 8 

    # START
    weitersuchen = True # Steuerung Suchschleife
    arbeitsvorrat = list() # Init Arbeitsvorrat
    arbeitsvorrat.append((0,START_POS[0],START_POS[1])) # Erster Job: Start-Pos (schritt=0, x, y)

    print("Starte Spielfeld: Start=%s, Ziel=%s" % (str(START_POS),str(TARGET_POS)))
    while GAMERUNNING:
        print_field()
        cnv.update()
        cnv.update_idletasks()    

        while weitersuchen:
            #print("Arbeitsvorrat: %s" % (str(arbeitsvorrat)))            
            if len(arbeitsvorrat) >= 1:
                arbeitsvorrat.sort() # da immer 1. pos in arbeitsvorrat 'Schrittzähler' ist, wird immer korrekt abgearbeitet
                if ((arbeitsvorrat[0][1] == TARGET_POS[0]) & (arbeitsvorrat[0][2] == TARGET_POS[1])):
                    weitersuchen = False
                    ziel_gefunden = (todo[0], arbeitsvorrat[0][1],arbeitsvorrat[0][2])                    
                else:
                    for todo in arbeitsvorrat:
                        #print("Prüfe: %s" % (str(todo)))
                        pos_pruefen(todo[0]+1,todo[1],todo[2])
                        arbeitsvorrat.remove(todo)
                        print_field()
                        break
            else:
                noway_flag=1
                break

        try:
            if noway_flag == 1:
                end_game("Error, Kein Weg zu finden...",9)
                break
        except:
            pass

        akt_wert=ziel_gefunden[0]
        akt_x=ziel_gefunden[1]
        akt_y=ziel_gefunden[2]
        weg_suchen = True

        input("Gefunden... weiter?")

        while weg_suchen:
            gesuchter_wert = akt_wert
            
            N=akt_y+1
            E=akt_x+1
            S=akt_y-1
            W=akt_x-1

            if ((N >= 0) & (N <= Y_ROWS-1)):
                if gesuchter_wert == FIELDVALUES[akt_x][N]:
                    akt_y = N

            if ((E <= X_COLS-1) & (E >= 0)):
                if gesuchter_wert == FIELDVALUES[E][akt_y]:
                    akt_x = E

            if ((S >= 0 ) & ( S <= Y_ROWS-1)):
                if gesuchter_wert == FIELDVALUES[akt_x][S]:
                    akt_y = S

            if ((W <= X_COLS-1 ) & ( W >= 0)):
                if gesuchter_wert == FIELDVALUES[W][akt_y]:
                    akt_x = W 

            N=akt_y+1
            E=akt_x+1
            S=akt_y-1
            W=akt_x-1

            if ((N >= 0) & (N <= Y_ROWS-1)):
                if "S" == FIELDVALUES[akt_x][N]:
                    GRID[akt_x][akt_y]=6                    
                    akt_y = N

            if ((E <= X_COLS-1) & (E >= 0)):
                if "S" == FIELDVALUES[E][akt_y]:
                    GRID[akt_x][akt_y]=6                    
                    akt_x = E

            if ((S >= 0 ) & ( S <= Y_ROWS-1)):
                if "S" == FIELDVALUES[akt_x][S]:
                    GRID[akt_x][akt_y]=6
                    akt_y = S

            if ((W <= X_COLS-1 ) & ( W >= 0)):
                if "S" == FIELDVALUES[W][akt_y]:
                    GRID[akt_x][akt_y]=6
                    akt_x = W 
                    
            #print("akt x:%d akt y:%d" % (akt_x,akt_y))
            if FIELDVALUES[akt_x][akt_y] == "S":
                end_game(str("Yay, Ziel wieder erreicht! x:%d y:%d " % (akt_x,akt_y)),11)      
                weg_suchen = False      
                input("Ende... Neustart?")
                break

            akt_wert = gesuchter_wert-1
            GRID[akt_x][akt_y]=6
            print_field()
