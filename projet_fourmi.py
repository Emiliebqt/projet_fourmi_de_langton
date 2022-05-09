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

 

