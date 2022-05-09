#import des modules 
import tkinter as tk
#constantes

#fonctions 
def demarer():
    pass

def next():
    pass

def pause():
    pass

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

#programme principal 

root=tk.Tk()
root.title("Fourmi de Langton")
#creation du canvas 
canvas=tk.Canvas(root, width=700, height=300, bg="white")

bouton_play=tk.Button(root, text="play", command=demarer)
bouton_next=tk.Button(root, text="next", command=next)
bouton_pause=tk.Button(root, text="pause", command=pause)

#definition des widgets 

canvas.grid(row=1, rowspam=10, column=1, columnspam=10)

bouton_play.grid(row=1, column=10)
bouton_next.grid(row=2, column=10)
bouton_pause.grid(row=3, column=10)

 


