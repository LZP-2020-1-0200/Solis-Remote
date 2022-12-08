
from tkinter import Widget, Frame

class SceneSwitcher():
    def __init__(self, parent:Widget) -> None:
        self.scenes:list[Frame]=[]
        self.parent:Widget=parent

    def addScene(self)->int:
        sc:Frame=Frame(self.parent)
        self.scenes.append(sc)
        if len(self.scenes)==1:
            sc.pack()
        return len(self.scenes)-1
    
    def getFrame(self,id:int)->Frame:
        return self.scenes[id]
    
    def switchTo(self, id:int)->None:
        for scene in self.scenes:
            scene.pack_forget()
        self.scenes[id].pack()

    

      
        