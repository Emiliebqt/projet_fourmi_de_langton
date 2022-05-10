#import des modules 
import tkinter as tk

#constantes
taille=1
DIM=100

#constantes du canvas

canvasSize=800 #taille en pixel du canvas 
nwidth = canvasSize // taille
nheight = canvasSize // taille
items = [[0] * nwidth for _ in range(nheight)]

position=(nheight // 2-10, nwidth // 2+19)
direction="N"

UNIT=canvasSize//DIM
#creation du canvas
#root=tk.Tk()
#root.title("Fourmi de Langton")
#canvas=tk.Canvas(root, width=canvasSize, height=canvasSize, bg="white")
#canvas.grid(row=0, column=1)

pause=True 
play=False #variable permettant de gere la bouple play/pause
DELAY=1


#fonctions 

def carre(i, j):
    x, y = j * taille, i * taille
    square = canvas.create_rectangle((x, y), (x + taille, y + taille), fill="black", outline='')
    return square


def dessin(position, direction, items):
    (ii, jj), direction = deplacement(position, direction, items)
    i, j = position
    square = items[i][j]

    if square == 0:
        square = dessin(i, j)
        items[i][j] = square
    else:
        canvas.delete(square)
        items[i][j] = 0

    return (ii, jj), direction

def deplacement():
    i, j = position

    if items[i][j] == 0:
        if direction == "N":
            r = (i, j + 1), "E"
        elif direction == "S":
            r = (i, j - 1), "W"
        elif direction == "E":
            r = (i + 1, j), "S"
        elif direction == "W":
            r = (i - 1, j), "N"
    else:
        if direction == "S":
            r = (i, j + 1), "E"
        elif direction == "N":
            r = (i, j - 1), "W"
        elif direction == "W":
            r = (i + 1, j), "S"
        elif direction == "E":
            r = (i - 1, j), "N"
    return r


def animation():
    global position, direction
    position, direction = dessin(position, direction)
    root.after(DELAY, animation)

def grille():
    for j in range(nwidth):
        canvas.create_line((j * UNIT, 0), (j * UNIT, canvasSize))
    for i in range(nheight):
        canvas.create_line((0, i * UNIT), (canvasSize, i * UNIT))


def anim(): #NE FONCTIONNE PAS 
    global position, direction
    position, direction = dessin(position, direction, items)
    root.after(DELAY, anim)

def demarer():
    """fontion permettant de lancer l'animation"""
    pass

def next():
    pass

def pause():
    """fonction permettant de mettre pause à l'animation"""
    global pause
    pause = False 

#curseur de vitesse
#root=tk.Tk()

#def curseur():
    #scVitesse = tk.Scale(root, orient='vertical', from_=1, to=100, resolution=0.01, length=100, label='Vitesse')
    #scVitesse.bind('<B1-Motion>', updateVitesse)
    #scVitesse.pack(padx=5, pady=5)
   # s=tk.Scale(root, orient='horizontal', from_=0, to=10, resolution=0.1, tickinterval=2, length=350, label='Volume (db)')


#programme principal 
root=tk.Tk()
root.title("Fourmi de Langton")
canvas=tk.Canvas(root, width=canvasSize, height=canvasSize, bg="white")
canvas.grid(row=1, column=1)

bouton_play=tk.Button(root, text="play", command=demarer) #.pack(side=tk.LEFT)
bouton_next=tk.Button(root, text="next", command=next)
bouton_pause=tk.Button(root, text="pause", command=pause)
#bouton_curseur=tk.Button(root, text="variation de vitesse", commande=curseur)

#definition des widgets 
#1canvas.grid(row=1, rowspan=10, column=1, columnspan=4)


bouton_play.grid(row=0, column=0)#ajouter padx=5 et pady+5 ??? 
bouton_next.grid(row=1, column=0)
bouton_pause.grid(row=2, column=0)
#bouton_curseur.grid(row=3, column=0)

grille()


root.mainloop()