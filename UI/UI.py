from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import bgcolor

class UI:
    def __init__(self) -> None:         
        #setup
        self.root = Tk()
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()

        #input 
        Label(self.root,text="Relation size").grid(column=0,row=0)
        self.relEntry = tk.Entry(self.root,textvariable="0",validate='all')
        self.relEntry.grid(column=1,row=0)
        self.relEntry['validatecommand'] = (self.relEntry.register(self.validate),'%P')
        Label(self.root,text="number of frames").grid(column=2,row=0)
        self.frameEntry = Entry(self.root,textvariable="1",validate='all')
        self.frameEntry.grid(column=3,row=0)
        self.frameEntry['validatecommand'] = (self.frameEntry.register(self.validate),'%P')
        Button(self.root,text="scramble").grid(column=0,row=1,padx=10)
        Button(self.root,text="sort").grid(column=1,row=1)

        #canvas
        canvas = Canvas(self.root,bg="white")
        canvas.grid(column=0,row=2,columnspan=20,rowspan=10,sticky=tk.N+tk.E+tk.S+tk.W)

        canvas.create_rectangle(1,1,20,20,fill="red")

        self.root.mainloop()

    def validate(self, P):
        try:
            float(P)
            return True
        except ValueError:
            return False
ui = UI()