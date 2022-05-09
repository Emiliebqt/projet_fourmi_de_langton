#import des modules 
import tkinter as tk
#constantes
#aaa
#fonctions 
def demarer():
    pass


#programme principal 

root=tk.Tk()
root.title("Fourmi de Langton")
#creation du canvas 
canvas=canvas(root, width=700, height=300, bg="white")

bouton_demarer=tk.Button(root, text="demarer")

#definition des widgets 

canvas.grid(row=1, rowspam=10, column=1, columnspam=10)

bouton_demarer.grid(row=1, column=10)

 

