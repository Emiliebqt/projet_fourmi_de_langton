#imports des modules
from random import gauss
import tkinter as tk
from tkinter import filedialog as fd
import os
from os.path import exists
from ast import literal_eval


#-------------------------------------------------------------------------------#
directory_name = 'Sauvegardes'
path = os.path.join(os.getcwd(), directory_name)
#Création du fichier de sauvegarde
file_counter = 0
file_name = f'sauvegarde{file_counter}.txt'

#Constantes

WIDTH = 900
HEIGHT = 900
MAX_SCALE = 150
MAX_DELAY = 500


#Direction et rotation

HAUT, BAS, GAUCHE, DROITE = 0, 1, 2, 3
ROTATION_DROITE = (DROITE, GAUCHE, HAUT, BAS)
ROTATION_GAUCHE = (GAUCHE, DROITE, BAS, HAUT)
MOVE = ((-1, 0), (1, 0), (0, -1), (0, 1))
COLORS = ('white', 'black')
WHITE, BLACK = 0, 1


#Variables

grid_scale = 40
offset_grid = WIDTH//grid_scale
grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
paused = True
delay_value = 70
iteration_counter = 0
ants = []
root = tk.Tk()
root.title("La fourmi de Langton")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
text_iteration_counter = tk.IntVar(root, value=iteration_counter)


# Fonctions

def create_ant(y, x): #création de la fourmie 
    global ants
    ant = (y, x, DROITE)
    ants.append(ant)




def valeur_compteur(): #fonction sur la valeur initiale du compteur 
    text_iteration_counter.set(iteration_counter)

def rules(): #création des règles de l'animation 
    global ants, grid, grid_scale, iteration_counter, text_iteration_counter
    for i, ant in enumerate(ants):
        y, x, direction = ant #direction que la fourmie doit prendre 
        if grid[y][x] == BLACK: #présentation des différents cas de figure en fonction de la couleur de la case 
            new_direction = ROTATION_GAUCHE[direction]
            grid[y][x] = WHITE
            update_GUI(y, x, 'white')
        else:
            new_direction = ROTATION_DROITE[direction]
            grid[y][x] = BLACK
            update_GUI(y, x, 'black')      
        offset_y, offset_x = MOVE[new_direction] #en fonction de la positon du pointeur 
        new_y, new_x = y+offset_y, x+offset_x
        if new_y >= grid_scale:
             new_y = 0
        if new_y < 0:
            new_y = grid_scale-1
        if new_x >= grid_scale:
             new_x = 0
        if new_x < 0:
            new_x = grid_scale-1
        update_GUI(new_y, new_x, 'red') #ajout de la fonction fourmie pour que les règles s'appliquent dessus 
        ants[i] = (new_y, new_x, new_direction)
        iteration_counter += 1
        valeur_compteur()


def update_GUI(y, x, color): #détermination de la valeur et couleur des fourmies qui seront placées
    canvas.itemconfig(grid_GUI[y][x], fill=color)


def clicked(event): #fonction qui permet de placer les fourmies 
    global offset_grid, ants
    x, y = int(event.x // offset_grid), int(event.y // offset_grid)
    if any((True for ant in ants if ant[0] == y and ant[1] == x)):
        return
    create_ant(y, x)
    update_GUI(y, x, 'red')


def iteration(): #fonction permettant la succession de toutes les étapes 
    global id_after, delay_value
    rules()
    id_after = canvas.after(delay_value, iteration)

def play(): #création de la fonction du bouton play/pause
    global paused, id_after
    if paused: 
        play_button.config(text="Pause")
        iteration()
    else:
        play_button.config(text="Play")
        canvas.after_cancel(id_after)
    paused = not paused


def next(): #fonction permettant de passer étape par étape 
    global paused #lorsque le bouton pause est activé 
    if not paused:
        return
    rules()


def draw_GUI(): #permet de dessiner les recrangles/cases 
    
    global grid_GUI, grid
    for i in range(grid_scale):
        y0 = offset_grid*i
        y1 = (offset_grid*i) + offset_grid
        for j in range(grid_scale):
            grid_GUI[i][j] = canvas.create_rectangle((offset_grid*j, y0), 
            ((offset_grid*j)+offset_grid, y1),
            fill=COLORS[grid[i][j]], outline='black')


def back(): #création du bouton retour une étape en arrière 
    global ants, grid, grid_scale, paused, iteration_counter, text_iteration_counter
    if not paused or iteration_counter == 0:
        return
    for i, ant in enumerate(ants):
        y, x, direction = ant
        offset_y, offset_x = MOVE[direction]
        new_y, new_x = y-offset_y, x-offset_x
        if new_y >= grid_scale:
            new_y = 0
        if new_y < 0:
            new_y = grid_scale-1
        if new_x >= grid_scale:
            new_x = 0
        if new_x < 0:
            new_x = grid_scale-1
        update_GUI(y, x, COLORS[grid[y][x]]) #on réutilise la fonction sur la couleur des cases pour connaitre les déplacements 
        if grid[new_y][new_x] == BLACK:
            new_direction = ROTATION_GAUCHE[direction]
            grid[new_y][new_x] = WHITE
            update_GUI(new_y, new_x, 'red')
        else:
            new_direction = ROTATION_DROITE[direction]
            grid[new_y][new_x] = BLACK
            update_GUI(new_y, new_x, 'red')
        ants[i] = (new_y, new_x, new_direction)
        iteration_counter -= 1
        valeur_compteur()

def entry_grid_scale(int): #création de la fonction permettant de changer l'echelle de la grille 
    global text_entry_scale, offset_grid, grid_scale, grid, grid_GUI, ants
    new_scale = text_entry_scale.get()
    if new_scale > MAX_SCALE:
        grid_scale = MAX_SCALE
    else:
        grid_scale = new_scale
    offset_grid = WIDTH//grid_scale
    grid = [[WHITE]*grid_scale for _ in range(grid_scale)]
    grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
    ants = []
    draw_GUI()
    text_entry_scale.set(int)


def save(): #création de la focntion permettant de sauvegarder à n'importe quel moment 
    global file_counter, file_name, grid, grid_scale, ants, offset_grid, iteration_counter
    if not exists(path):
        os.mkdir(path)
    for files in os.listdir(path):  
        if files == file_name:
            file_counter += 1
            file_name = f'save{file_counter}.txt'
    with open(os.path.join(path, file_name), 'w') as file:
        file.write(
            f'{grid_scale}\n{iteration_counter}\n{offset_grid}\n{ants}\n{grid}')
        file.close()


def delay(int): #fonction permettant d'augmenter la vitesse d'execution
    global text_entry_delay, delay_value
    delay_value = text_entry_delay.get()
    if delay_value > MAX_DELAY:
        delay_value = MAX_DELAY
    text_entry_delay.set(int)


def load(): #permet d'enregistrer sur l'ordinateur 
    global grid, grid_scale, ants, offset_grid, grid_GUI, iteration_counter
    lines = []
    load_file = fd.askopenfilename(initialdir=path,
                                   title="Select a save",
                                   filetypes=(("Text files",
                                               "*.txt*"),
                                              ("all files",
                                               "*.*")))
    if load_file:
        load_file = load_file[load_file.rfind('sauvegarde'):]
        with open(os.path.join(path, load_file), 'r') as file:
            content = file.readlines()
        for line in content:
            lines.append(line)
        print(lines)
        grid_scale = int(lines[0])
        grid_GUI = [[WHITE]*grid_scale for _ in range(grid_scale)]
        iteration_counter = int(lines[1])
        offset_grid = int(lines[2])
        ants = literal_eval(lines[3])
        grid = literal_eval(lines[4])
        valeur_compteur()
        draw_GUI()



def GUI_widgets(): #fonction comprenannt la création des widgets 
    global text_entry_scale, text_entry_delay, play_button, save_button, iteration_counter

    # Noms des boutons à valeurs modifiables
    labelframe_delay = tk.LabelFrame(root,
                                     text='Change la vitesse de la fourmie')
    labelframe_scale = tk.LabelFrame(root,
                                     text='Changes la taille de la grille')

    # Créations des boutons 
    quit_button = tk.Button(root, text='Quit', command=root.quit)
    play_button = tk.Button(root, text='Play', command=play)
    next_button = tk.Button(root, text='Next', command=next)
    save_button = tk.Button(root, text='Save', command=save)
    load_button = tk.Button(root, text='Load', command=load)
    back_button = tk.Button(root, text='Back', command=back)
    scale_button = tk.Button(
        labelframe_scale, text='Valider', command=lambda: entry_grid_scale(0))
    delay_button = tk.Button(
        labelframe_delay, text='Valider', command=lambda: delay(0))
    # IntVar
    text_entry_scale = tk.IntVar()
    text_entry_delay = tk.IntVar()
    # Label
    label_interation_counter = tk.Label(
        root, textvariable=text_iteration_counter)
    # Entry
    delay_entry = tk.Entry(labelframe_delay, textvariable=text_entry_delay)
    scale_text = tk.Entry(labelframe_scale, textvariable=text_entry_scale)

    # placement des boutons 
    canvas.grid(column=1, row=1, columnspan=15, rowspan=15)
    play_button.grid(row=0, column=0)
    next_button.grid(row=1, column=0)
    back_button.grid(row=2, column=0)
    save_button.grid(row=3, column=0)
    load_button.grid(row=4, column=0)
    delay_entry.grid(row=5, column=0)
    delay_button.grid(row=6, column=0)
    scale_text.grid(row=7, column=0)
    labelframe_scale.grid(row=8, column=0)
    labelframe_delay.grid(row=9, column=0)
    scale_button.grid(row=10, column=0)
    quit_button.grid(row=11, column=0)
    label_interation_counter.grid(row=12, column=0)

    # Bind
    canvas.bind('<Button-1>', clicked)

################
# Programme principal #
################


def main(): #permet de mettre en route et de relier les fonctions ensembles
    '''Main program with tkinter instructions'''
    draw_GUI()
    GUI_widgets()
    root.mainloop()


if __name__ == '__main__':
    main()

#pour la réalisation du projet : utilisation de videos pour l'utilisation tkinter 
#ainsi que différents sites (nombreux) sur les différentes commandes, definitions etc