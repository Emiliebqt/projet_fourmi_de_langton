#import des modules 
import tkinter as tk

#constantes

pause=True 
canvasSize=800 #taille en pixel du canvas 
play=False #variable permettant de gere la bouple play/pause


#fonctions 



def demarer():
    """fontion permettant de lancer l'animation"""
    pass

def next():
    pass

def pause():
    """fonction permettant de mettre pause à l'animation"""
    global pause
    pause = False 

#programme principal 

root=tk.Tk()
root.title("Fourmi de Langton")
#creation du canvas 
canvas=tk.Canvas(root, width=canvasSize, height=canvasSize, bg="white")

bouton_play=tk.Button(root, text="play", command=demarer)
bouton_next=tk.Button(root, text="next", command=next)
bouton_pause=tk.Button(root, text="pause", command=pause)

#definition des widgets 

canvas.grid(row=1, column=1)

bouton_play.grid(row=0, column=0) #ajouter padx=5 et pady+5 ??? 
bouton_next.grid(row=1, column=0)
bouton_pause.grid(row=2, column=0)

root.mainloop()