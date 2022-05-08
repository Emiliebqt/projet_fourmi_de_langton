# projet_fourmi_de_langton

from tkinter import *
from math import *
import cmath
from tkinter.messagebox import *
import random

white = 'snow'
black = 'gray1'
red = 'red'
blue = 'dodger blue'
orange = 'orange'

class Ant:
    def __init__(self, pos, dir):
        self.pos=pos
        self.dir=dir
        self.onBoard=True
        
    def walk(self):
        if self.dir == 0:#droite
            self.pos[0] +=1
        elif self.dir == 1:#tout droit
            self.pos[1] -=1
        elif self.dir == 2:#gauche
            self.pos[0] -=1
        elif self.dir == 3:#demi tour
            self.pos[1] +=1
        if self.pos[0]>gridSize-1:
            self.pos[0]=0 
        if self.pos[0]<0:
            self.pos[0]=gridSize-1 
        if self.pos[1]<0:
            self.pos[1]=gridSize-1
        if self.pos [1]>gridSize-1:
            self.pos[1]=0

        
    def invwalk(self):
        if self.dir == 0:#droite
            self.pos[0] -=1
        elif self.dir == 1:#tout droit
            self.pos[1] +=1
        elif self.dir == 2:#gauche
            self.pos[0] +=1
        elif self.dir == 3:#demi tour
            self.pos[1] -=1
        if self.pos[0]>gridSize-1:
            self.pos[0]=0 
        if self.pos[0]<0:
            self.pos[0]=gridSize-1 
        if self.pos[1]<0:
            self.pos[1]=gridSize-1
        if self.pos [1]>gridSize-1:
            self.pos[1]=0
            
    def changeCellDir(self):
        global cellType
        cellBoard[self.pos[0]][self.pos[1]] += 1
        cellBoard[self.pos[0]][self.pos[1]] = cellBoard[self.pos[0]][self.pos[1]]%len(cellType)
            
    def interactWithCell(self):
        global cellType
        #print("je suis sur la case: ", self.pos)
        self.dir+=cellType[cellBoard[self.pos[0]][self.pos[1]]]
        self.dir = self.dir%4
        self.changeCellDir()
        
    def draw(self, canvas):
        if self.onBoard == True:
                rayon = largeurCell/2.2#rayon du triangle equilateral
                ptCenter = ((self.pos[0]+1/2)*largeurCell, (self.pos[1]+1/2)*largeurCell)
                angle = -(pi/2*self.dir)%(2*pi)#angle en radians en fonction de la direction
                pt1 = (ptCenter[0]+cos(pi*2/3)*rayon*1.5, ptCenter[1]-sin(pi*2/3)*rayon)
                pt2 = (ptCenter[0]+cos(pi*2/3)*rayon*1.5, ptCenter[1]+sin(pi*2/3)*rayon)
                pt3 = (ptCenter[0]+1.1*rayon, ptCenter[1])
                pt1 = rotateCoordo(ptCenter, pt1, angle)
                pt2 = rotateCoordo(ptCenter, pt2, angle)
                pt3 = rotateCoordo(ptCenter, pt3, angle)
                canvas.create_polygon(pt1[0], pt1[1], pt2[0], pt2[1], pt3[0], pt3[1], fill=red)  
                    
##Variables

fen = Tk()
CanvasSize = 1000# taille en pixel du canvas
gridSize = 100 #taille de de la grille en cases
largeurCell = CanvasSize/gridSize #largeur d'une cellule
vitesse = 500  #en ms 
compteur = 0 #compteur d'iteration de la boucle 
cellBoard = [] #tableau de cellules
tilt = Ant([0,0],0) #fourmi
play = False # variable qui permet de gerer la boucle play/pause

cellType = [+1,-1] # type de la cellule representé par un tableau conteant les direction sucesive que va indiquer la cellule à la fourmi
""" base : pour inverser la direction de la cellule [+1,-1]
    cercle :[+1,2,-1,0]
    ...au choix de l'utilisateur """
genMode = "fill"#mode de generation des cellules
""" aleatoire : pour generer aleatoirement
    fill: remplir de casse selon le type """
## fonctions boutons 

def callbackExit(fenetre):#s'ouvre pour fermer la fenetre (bonus)
    if askyesno('exit', 'voulez vous vraiment quitter ?'):
        fenetre.destroy()
        
def updateVitesse(event): #gère le curseur de vitesse 
    global vitesse
    vitesse = int(1000/scVitesse.get()**0.5-scVitesse.get())
    #vitesse = int(1000/(e**scVitesse.get()/e))
    
def playClick(event):#change la variable play quand on appui sur le bouton 
    global play
    if play == False:
        play = True
        boucle()

def playNext(event):#change la variable play quand on appui sur le bouton 
    global play
    if play == False:
        etape()
    else:
        play = False
        etape()

def playInv(event):#change la variable play quand on appui sur le bouton 
    global play
    if play == False:
        invetape()
    else:
        play = False
        invetape()
        
def pauseClick(event):#change la variable play quand on appui sur le bouton pause
    global play
    play = False

def setCellType(type):#change le type de la cellule
    global cellType, genMode
    cellType = type
    init(genMode, tilt)
    
def setGenMode(mode):
    genMode = mode
    print(genMode)
    init(genMode, tilt)
    showinfo("info", "la grille à été générée")
##fonction qui gère la creation d'une nouvelle fenetre pour demandé à l'utilisateur un type de cellule personalisé
def setTypeModeUtilisateur(fenetre, ActuelCellType):#retourne un tableau de valeur conteant les direction sucessive que va prendre la case choisi par l'utilisateur
    newFen = Toplevel(fenetre)#creation d'un nouvelle fenetre
    newCellType = [ActuelCellType]
    #creation de 2 frames pour gerer la demande
    FrameNb = Frame(newFen, borderwidth=2, relief=GROOVE)
    labelNb = Label(FrameNb, text="nombre de direction")
    labelNb.pack(side=LEFT, padx=5, pady=5)
    entry = Spinbox(FrameNb, from_=1, to=10)
    entry.pack(side=RIGHT, padx=5, pady=5)
    FrameNb.pack(side=LEFT, padx=10, pady=10)

    FrameValue = Frame(newFen, borderwidth=2, relief=GROOVE)
    SpinboxValue = []
    
    def valider(type):#fonction du bouton valider qui reagie en fonction de la frame affichée
        if FrameNb.winfo_exists() == 1:
            nb = int(entry.get())
            for i in range(nb):
                l = Label(FrameValue, text="direction "+str(i) + " :")
                l.grid(row=i, padx=5, pady=5)
                SpinboxValue.append(Spinbox(FrameValue, from_=-1, to=2))
            for i in range(nb):
                SpinboxValue[i].grid(row=i, column= 1, padx=5, pady=5)
                
            FrameNb.destroy()
            FrameValue.pack(side=LEFT, padx=10, pady=10)
        else:
            type[0] = []
            for s in SpinboxValue:
                type[0].append(int(s.get()))
            FrameValue.destroy()
            newFen.quit()
             
    def quitter():
        newFen.quit()
        print ("quitter",newCellType)
    
    boutonAnnuler = Button(newFen, text = "annuler", command= quitter)
    boutonAnnuler.pack(side=RIGHT, padx=10, pady=10)
    boutonValider = Button(newFen, text = "Valider", command=lambda: valider(newCellType))
    boutonValider.pack(side=RIGHT, padx=10, pady=10)
    
    
    newFen.mainloop()
    newFen.destroy()
    print ("finFonction",newCellType)
    return newCellType[0]# elle retourne le nouveau type de la cellule defini par l'utilisateur
      
##creation de la fenetre

fen.title('fourmi de langton')
# On crée un canevas
canvas = Canvas(fen, width=CanvasSize, height=CanvasSize, background="white")
canvas.pack(side=RIGHT, padx=5, pady=5)

#on crée une frame contenant les boutons 
frameBoutons = LabelFrame(fen, text="Options et boutons")
frameBoutons.pack(side=LEFT, padx=5, pady=5, fill=BOTH, expand="yes" )

labelCompteur = Label(frameBoutons, text="Compteur : "+str(compteur) )
labelCompteur.pack()
#bouton play
btPlay = Button(frameBoutons, text ='Play')
btPlay.bind('<Button-1>', playClick)
btPlay.pack(padx=5, pady=5)
#bouton next
btPlay = Button(frameBoutons, text ='Next')
btPlay.bind('<Button-1>', playNext)
btPlay.pack(padx=5, pady=5)
#bouton inverse
btPlay = Button(frameBoutons, text ='Inverse')
btPlay.bind('<Button-1>', playInv)
btPlay.pack(padx=5, pady=5)
#bouton pause
btPause = Button(frameBoutons, text ='pause')
btPause.bind('<Button-1>', pauseClick)
btPause.pack(padx=5, pady=5)
#curseur de vitesse
scVitesse = Scale(frameBoutons, orient='vertical', from_=1, to=100, resolution=0.01, length=100, label='Vitesse')
scVitesse.bind('<B1-Motion>', updateVitesse)
scVitesse.pack(padx=5, pady=5)
#dessiner l'animation en continu ou non 
varCheckDraw = IntVar()
checkDraw = Checkbutton(frameBoutons, text="dessin en continu", variable= varCheckDraw)
varCheckDraw.set(1)
checkDraw.pack(padx=5, pady=5)
    
"""-----creation d'un menu-----"""
menuBar = Menu(fen)
#menu pour init avec le mode voulu
menuGen = Menu(menuBar, tearoff=0)
menuGen.add_command(label="aleatoire", command=lambda: setGenMode("aleatoire"))
menuGen.add_command(label="fill", command=lambda: setGenMode("fill"))
menuBar.add_cascade(label="mode de generation", menu=menuGen )
#menu pour le type de cellule
menuType = Menu(menuBar, tearoff=0)
menuType.add_command(label="base", command=lambda: setCellType([1,-1]))
menuType.add_command(label="cercle", command=lambda: setCellType([1,2,-1,0]))
menuType.add_command(label="choix", command=lambda: setCellType(setTypeModeUtilisateur(fen,cellType)))
menuBar.add_cascade(label="mode de Swap", menu=menuType )

menuBar.add_command(label="Quitter", command=lambda: callbackExit(fen))
fen.config(menu = menuBar)
##Fonctions tableau

def genAlea():#genere la grille aleatoirement en fonction du type de la cellule
    global cellBoard, cellType
    fillArray(1)
    for i in range(gridSize):
        for j in range(gridSize):
            cellBoard[i][j] = random.randint(0,len(cellType)-1)#choisi un index aleatoire parmis le tableau cellType
    
def fillArray(value):#rempli le tableau par l'index choisi
    global cellBoard
    cellBoard = []
    for i in range(gridSize):
        raw = []
        for j in range(gridSize):
            raw.append(value)
        cellBoard.append(raw)
        
##fonctions draw 
def rotateCoordo(rotatePt, pt, angle):#fonction utilisant les nb complexes pour faire tourner un pt en rotation autour d'un autre
    cangle = e**(angle*complex(0,1)) 
    ptComplex = complex(pt[0], pt[1])
    center = complex(rotatePt[0], rotatePt[1])
    newCoordo = cangle * (ptComplex - center) + center
    return (newCoordo.real, newCoordo.imag)#retourne les nouvelles coordonnées du pt, cette fonction est utilisée pour faire tourner le triangle symbolisant la fourmi
    
def drawCellBoard(canvas):#dessine toute les cases
    for i in range(len(cellBoard)):
        for j in range(len(cellBoard)):
            drawCell(i, j, canvas)

def drawCell(posX, posY, canvas):#dessine une case
    global cellType, cellBoard, largeurCell
    #change la couleur en fonction de la direction
    color = None
    if cellType[cellBoard[posX][posY]] == -1:#droite
        color = black
    elif cellType[cellBoard[posX][posY]] == 0:#tout droit
        color = orange
    elif cellType[cellBoard[posX][posY]] == 1:#gauche
        color = white
    elif cellType[cellBoard[posX][posY]] == 2:#demi tour
        color =  blue
    else:
        print("error : value:", cellType[cellBoard[posX][posY]])
    canvas.create_rectangle(posX*largeurCell, posY*largeurCell, (posX+1)*largeurCell-1, (posY+1)*largeurCell-1, fill = color, outline = black)
        
##fonctions principales

def init(mode, ant):  #fonction d'initialisation lancer au debut pour generer une nouvelle grille et fourmi
    global play, compteur, labelCompteur, cellBoard
    play = False
    compteur = 0 
    labelCompteur.config(text="Compteur : "+str(compteur))
    if mode == "aleatoire":
        genAlea()
    elif mode == "fill":
        fillArray(0)
    ant.pos[0] = gridSize//2
    ant.pos[1] = gridSize//2
    ant.dir = 0
    ant.onBoard = True
    
    drawCellBoard(canvas)
    ant.draw(canvas)

def boucle():#fonction qui tourne en boucle
    global play, compteur, labelCompteur, varCheckDraw
    compteur+=1#on incremente le compteur
    labelCompteur.config(text="Compteur : "+str(compteur))#on affiche le nouveau texte du compteur
    tilt.interactWithCell()#la fourmi interagie pour changer de direction
    if(varCheckDraw.get()==1):#si on doit dessiner 
        drawCell(tilt.pos[0], tilt.pos[1], canvas)#on dessine la case ou se trouvait la fourmi pour effacer le triangle
        tilt.walk()#on fait avancer la fourmi
        tilt.draw(canvas)#on dessine sa nouvelle position
    else:
        tilt.walk()#sinon on ne dessine pas on fait juste avancer la fourmi
    
    fen.update_idletasks()#utilisé pour mettre à jour les evenements de la fenetre
    fen.update()
    
    if tilt.onBoard== True:
        if play == True:
            fen.after(vitesse, boucle)#relance la boucle tant que la variable play=True
        else:
            drawCellBoard(canvas)
            tilt.draw(canvas)
    else:#on arrete si la fourmi sort du cadre 
        play = False
        drawCellBoard(canvas)
def etape():
    global play, compteur, labelCompteur, varCheckDraw
    compteur+=1#on incremente le compteur
    labelCompteur.config(text="Compteur : "+str(compteur))#on affiche le nouveau texte du compteur
    tilt.interactWithCell()#la fourmi interagie pour changer de direction
    if(varCheckDraw.get()==1):#si on doit dessiner 
        drawCell(tilt.pos[0], tilt.pos[1], canvas)#on dessine la case ou se trouvait la fourmi pour effacer le triangle
        tilt.walk()#on fait avancer la fourmi
        tilt.draw(canvas)#on dessine sa nouvelle position
    else:
        tilt.walk()#sinon on ne dessine pas on fait juste avancer la fourmi
    
    fen.update_idletasks()#utilisé pour mettre à jour les evenements de la fenetre
    fen.update()

def invetape():
    global play, compteur, labelCompteur, varCheckDraw
    compteur-=1#on incremente le compteur
    labelCompteur.config(text="Compteur : "+str(compteur))#on affiche le nouveau texte du compteur
    tilt.interactWithCell()#la fourmi interagie pour changer de direction
    if(varCheckDraw.get()==1):#si on doit dessiner 
        drawCell(tilt.pos[0], tilt.pos[1], canvas)#on dessine la case ou se trouvait la fourmi pour effacer le triangle
        tilt.invwalk()#on fait avancer la fourmi
        tilt.draw(canvas)#on dessine sa nouvelle position
    else:
        tilt.invwalk()#sinon on ne dessine pas on fait juste avancer la fourmi
    
    fen.update_idletasks()#utilisé pour mettre à jour les evenements de la fenetre
    fen.update()
##lancement du programme 
init(genMode, tilt)
fen.mainloop()
message.txt
