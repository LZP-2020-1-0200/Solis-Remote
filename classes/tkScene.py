
from tkinter import * 


class Scene():

    def __init__(self,parent:Widget):
        self.main=Frame(parent)

    
    def close(self):
        self.main.pack_forget()

    def open(self):
        self.main.pack()
    
class SceneSwitcher():
    def __init__(self) -> None:
        self.scenes:list[Scene]=[]

    def addScene(self,parent:Widget)->int:
        sc:Scene=Scene(parent)
        self.scenes.append(sc)
        return len(self.scenes)-1
    
    def getFrame(self,id:int)->Frame:
        return self.scenes[id].main
    
    def switchTo(self, id:int)->None:
        for scene in self.scenes:
            scene.close()
        self.scenes[id].open()

    

      
        