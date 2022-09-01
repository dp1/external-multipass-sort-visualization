from contextlib import redirect_stderr
from numbers import Integral
import numbers
from subprocess import CREATE_NEW_CONSOLE
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
        self.relEntry.insert(END,"1")
        self.relEntry['validatecommand'] = (self.relEntry.register(self.validate),'%P')
        Label(self.root,text="number of frames").grid(column=2,row=0)
        self.frameEntry = Entry(self.root,textvariable="1",validate='all')
        self.frameEntry.grid(column=3,row=0)
        self.frameEntry.insert(END,"1")
        self.frameEntry['validatecommand'] = (self.frameEntry.register(self.validate),'%P')
        Button(self.root,text="scramble").grid(column=0,row=1,padx=10)
        Button(self.root,text="sort").grid(column=1,row=1)
        Button(self.root,text="set",command=lambda:self.genFrames()).grid(column=2,row=1)

        #canvas
        self.canvas = Canvas(self.root,bg="white")
        self.canvas.grid(column=0,row=2,columnspan=20,rowspan=10,sticky=tk.N+tk.E+tk.S+tk.W)

        self.root.mainloop()

    def frames(self, n: numbers,row,outputFrame):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        posx=int(width/2)
        posy=int(height/2)+(row*30)

        posx = posx-int(n/2)*22
        if n%2==1: 
            posx = posx-11
        frames=[]
        for i in range(n):
            frame = myFrame(posx=posx,posy=posy,canvas=self.canvas,color="red")
            posx+=22
            frames.append(frame)
        posx+=10
        if(outputFrame):
            frames.append(myFrame(posx=posx,posy=posy,color="green",canvas=self.canvas))
        pass

    def genFrames(self):
        self.canvas.delete("all")
        self.canvas.update()
        self.frames(n=int(self.frameEntry.get()),row=0,outputFrame=True)
        self.frames(n=int(self.relEntry.get()),row=1,outputFrame=False)

    def validate(self, P):
        try:
            float(P)
            return True
        except ValueError:
            return False

class frameItem:
    def __init__(self,posx,posy) -> None:
        self.color = "green"
        self.x = posx
        self.y = posy
        pass

class myFrame:
    def __init__(self,posx,posy,color:str, canvas: Canvas) -> None:
        #position of upper left corner of frame
        self.x = posx
        self.y = posy

        if(color == ""):
            self.color = "red"
        else:
            self.color = color

        canvas.create_rectangle(self.x,self.y,self.x+20,self.y+20,fill=self.color)
        pass
ui = UI()