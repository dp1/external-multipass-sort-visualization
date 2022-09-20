from time import sleep
from tkinter import ttk
import tkinter as tk
from typing import List
from visualizer.data import StateSnapshot, Frame
from visualizer.sort_algorithm import Sort

class UI:
    def __init__(self) -> None:
        #setup
        self.root = tk.Tk()
        self.root.title("Multipass sort")

        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()

        self.scale = None
        self.generated = False
        self.snapShots=[]
        self.pos = 0
        self.playC = False
        self.relSize = 0
        self.update = False

        #input
        tk.Label(self.root,text="Relation size").grid(column=0,row=0)
        self.relEntry = tk.Entry(self.root,textvariable="0",name="relationSize")
        self.relEntry.grid(column=1,row=0)
        self.relEntry.insert(tk.END,"20")
        # self.relEntry['validatecommand'] = (self.relEntry.register(self.validate),'%P','%W')
        # self.relEntry['invalidcommand'] = (self.relEntry.register(self.invalidInput),'%P','%W')
        tk.Label(self.root,text="number of frames").grid(column=2,row=0)
        self.frameEntry = tk.Entry(self.root,textvariable="1",name="framesNumber")
        self.frameEntry.grid(column=3,row=0)
        self.frameEntry.insert(tk.END,"5")
        # self.frameEntry['validatecommand'] = (self.frameEntry.register(self.validate),'%P','%W')
        # self.frameEntry['invalidcommand'] = (self.frameEntry.register(self.invalidInput),'%P','%W')
        tk.Button(self.root,text="sort",command=lambda:self.sort()).grid(column=1,row=1)
        self.playB = None

        #canvas
        self.canvas = tk.Canvas(self.root,bg="white")
        self.canvas.grid(column=0,row=2,columnspan=20,rowspan=10,sticky=tk.N+tk.E+tk.S+tk.W)

        # Arrow movement
        self.frm.bind('<Left>', lambda _: self.scale.set(max(0, self.scale.get() - 1)) if self.scale else None)
        self.frm.bind('<Right>', lambda _: self.scale.set(max(0, self.scale.get() + 1)) if self.scale else None)

        # Restore focus by clicking on the canvas
        self.canvas.bind("<Button-1>", lambda _: self.frm.focus_set())

        self.loop()

    def frames(self, n: int, buffers: List[Frame],row):
        relationSize = self.relSize
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        posx=int(width/2)
        posy=int(height/2)+(row*30)-50

        posx = posx-int(n/2)*22
        if n%2==1:
            posx = posx-11
        frames=[]
        for i in range(n):
            frame = myFrame(posx=posx,posy=posy,canvas=self.canvas, color="green")
            if(len(buffers)>0):
                buffer = buffers[i]
                bLen = 3
                for val in buffer.data:
                    if not val.empty:
                        data = val.value
                        pos = data/(relationSize*4)
                        if pos > 1: pos = 1
                        r = 255
                        g = int(255 * (1-pos))
                        b = int(255 * pos)
                        item = frameItem(posx=posx,posy=posy+(bLen*5),canvas=self.canvas,color=colorString(r,g,b))
                        bLen-=1
            posx+=22
            frames.append(frame)
        pass

    def updateCanvas(self):
        if(self.generated):
            snapPos = int(self.scale.get())

            if (snapPos != self.pos):
                #self.sort()
                self.pos = snapPos
                self.update = True

    def genFromSnapshot(self, state: StateSnapshot):
        self.canvas.delete("all")
        frames = len(state.buffer)
        relation = len(state.relation)

        self.frames(n=frames,buffers=state.buffer,row=0)
        self.frames(n=relation,buffers=state.relation,row=1)

        description = self.canvas.create_text(120,10,text=state.description)
        self.update = False or self.playC

    def sort(self):

        self.checkInput()

        self.playC = False
        self.pos = 0
        try:
            self.relSize = int(self.relEntry.get())
            frameSize = int(self.frameEntry.get())
            self.oldFrmNum = frameSize
            self.oldRelNum = self.relSize
            if self.relSize<2 or frameSize<2:
                raise ValueError
        except ValueError:
            self.canvas.create_text(20,20,text="Invalid Input, both need to be an integer >2")
            return

        sort = Sort(B = self.relSize, F = frameSize)
        sort.sort()
        self.canvas.delete("all")
        self.canvas.update()
        self.snapShots = sort.steps

        self.scale = tk.Scale(self.root,from_=0,to=len(sort.steps)-1,orient=tk.HORIZONTAL,length=200)
        self.scale.grid(column=0,row=10)
        self.generated = True
        self.playB = tk.Button(self.root,text="Play",command=lambda:self.play())
        self.playB.grid(column=1,row=10)
        self.update = True

        self.frm.focus_set()

    def play(self):
        self.playC = not self.playC
        self.pos = 0
        self.update = True

    def checkInput(self):
        rel = self.relEntry.get()
        if(rel == ""):
            self.relEntry.insert(tk.END,"2")
        else:
            try:
                r = int(rel)
                if r < 2 or r > 30:
                    self.relEntry.delete(0,tk.END)
                    self.relEntry.insert(tk.END, "2" if r < 2 else "30")
            except ValueError:
                self.relEntry.delete(0,tk.END)
                self.relEntry.insert(tk.END,"2")


        frm = self.frameEntry.get()
        if(frm == ""):
            self.frameEntry.insert(tk.END,"2")
        else:
            try:
                f = int(frm)
                if f < 2 or f > 30:
                    self.frameEntry.delete(0,tk.END)
                    self.frameEntry.insert(tk.END, "2" if f < 2 else "30")
            except ValueError:
                self.frameEntry.delete(0,tk.END)
                self.frameEntry.insert(tk.END,"2")

    def draw(self):
        if(self.update):
            self.genFromSnapshot(state=self.snapShots[self.pos])


    def loop(self):
        while(True):
            #check valid input
            #check if need redraw
            self.updateCanvas()
            #draw
            self.draw()

            if(self.playC):
                self.pos+=1
                if(self.pos >= len(self.snapShots)):
                    self.playC=False
                    self.update = False
                self.scale.set(self.pos)

                frameTime = min(0.5, 10 / len(self.snapShots))
                sleep(frameTime)

            if self.playB:
                self.playB.config(text='Pause' if self.playC else 'Play')

            self.root.update_idletasks()
            self.root.update()

class frameItem:
    def __init__(self,posx,posy, canvas: tk.Canvas, color = "green") -> None:
        self.color = color
        self.x = posx
        self.y = posy

        canvas.create_rectangle(self.x,self.y,self.x+20,self.y+5,fill=self.color)

class myFrame:
    def __init__(self,posx,posy,color:str, canvas: tk.Canvas,height=20) -> None:
        #position of upper left corner of frame
        self.x = posx
        self.y = posy

        if(color == ""):
            self.color = "green"
        else:
            self.color = color

        canvas.create_rectangle(self.x,self.y,self.x+20,self.y+height,fill=self.color)

def colorString(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{r:02x}{g:02x}{b:02x}'
