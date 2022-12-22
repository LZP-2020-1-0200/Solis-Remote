
from tkinter import Misc, Frame

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

class SceneSwitcher():
    def __init__(self, parent:Misc) -> None:
        self._scenes:list[Frame]=[]
        self._parent:Misc=parent

    def addScene(self)->int:
        sc:Frame=Frame(self._parent)
        self._scenes.append(sc)
        if len(self._scenes)==1:
            sc.pack()
        return len(self._scenes)-1
    
    def getFrame(self,id:int)->Frame:
        return self._scenes[id]
    
    def switchTo(self, id:int)->None:
        for scene in self._scenes:
            scene.pack_forget()
        self._scenes[id].pack()
        log.info(f"Switching to scene [{id}]")


    

      
        