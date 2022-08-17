from cProfile import label
from tkinter import *
from tkinter import ttk
import tkinter as tk

#setup
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

#input
ttk.Label(root,text="Relation size").grid(column=0,row=0)
ttk.Entry(root).grid(column=1,row=0)
ttk.Label(root,text="frame number").grid(column=0,row=1)
ttk.Entry(root).grid(column=1,row=1)
ttk.Button(root,text="sort").grid(column=2,row=0)

#Visualization
canvas = tk.Canvas(root,bg="white",height=480,width=900)
canvas.grid(column=2,row=2)


root.mainloop()