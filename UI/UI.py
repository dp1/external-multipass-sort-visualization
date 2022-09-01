from logging import root
import numbers
from tkinter import *
from tkinter import ttk
import tkinter as tk
from typing import List
import sys
sys.path.append("../external-multipass-sort-visualization")
from visualizer.data import StateSnapshot
from visualizer.sort_algorithm import Sort
from visualizer.data import Tuple

class UI:
    def __init__(self) -> None:
        #setup
        self.root = Tk()
        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        self.scale = 0
        self.generated = False
        self.snapShots=[]

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
        Button(self.root,text="sort",command=lambda:self.sort()).grid(column=1,row=1)

        #canvas
        self.canvas = Canvas(self.root,bg="white")
        self.canvas.grid(column=0,row=2,columnspan=20,rowspan=10,sticky=tk.N+tk.E+tk.S+tk.W)


        self.loop()

    def frames(self, n: numbers, buffers: List[Frame],row):
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
            if(len(buffers)>0):
                buffer = buffers[i]
                bLen = 4
                for val in buffer.data:
                    if val.empty:
                        bLen-=1
                h = int(20 * ((bLen)/4))
                fill = myFrame(posx=posx,posy=posy+(20-h),height=h,canvas=self.canvas,color="green")
            posx+=22
            frames.append(frame)
        # posx+=10
        # if(outputFrame):
        #     frames.append(myFrame(posx=posx,posy=posy,color="green",canvas=self.canvas))
        pass

    def genFromSnapshot(self, state: StateSnapshot):
        frames = len(state.buffer)
        relation = len(state.relation)

        self.frames(n=frames,buffers=state.buffer,row=0)
        self.frames(n=relation,buffers=state.relation,row=1)
        pass

    def sort(self):
        sort = Sort(B = int(self.relEntry.get()), F = int(self.frameEntry.get()))
        sort.sort()
        self.canvas.delete("all")
        self.canvas.update()
        # self.genFromSnapshot(state=sort.steps[0])
        self.snapShots = sort.steps

        self.scale = Scale(self.root,from_=0,to=len(sort.steps)-1,orient=HORIZONTAL,length=200)
        self.scale.grid(column=0,row=10)
        self.generated = True
        #self.scale.after(24,self.genFromSnapshot(state=sort.steps[self.scale.get()]))

    def validate(self, P):
        try:
            float(P)
            return True
        except ValueError:
            return False

    def loop(self):
        while(True):
            self.canvas.delete("all")
            if(self.generated):
                self.genFromSnapshot(state=self.snapShots[self.scale.get()])

            self.root.update_idletasks()
            self.root.update()

class frameItem:
    def __init__(self,posx,posy) -> None:
        self.color = "green"
        self.x = posx
        self.y = posy
        pass

class myFrame:
    def __init__(self,posx,posy,color:str, canvas: Canvas,height=20) -> None:
        #position of upper left corner of frame
        self.x = posx
        self.y = posy

        if(color == ""):
            self.color = "red"
        else:
            self.color = color

        canvas.create_rectangle(self.x,self.y,self.x+20,self.y+height,fill=self.color)
        pass