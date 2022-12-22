from classes.event import CustomEvent
from tkinter import Button, filedialog, Frame, Misc
from helpers.configuration import *
from classes import sessionData
from classes.logger import Logger
import logging

log:logging.Logger=Logger(__name__).get_logger()

onload:CustomEvent=CustomEvent()
onload.bind(lambda:log.info("onload called"))
oncreate:CustomEvent=CustomEvent()
oncreate.bind(lambda:log.info("oncreate called"))
ontomenu:CustomEvent=CustomEvent()
ontomenu.bind(
    lambda:log.info("ontomenu called"))


class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        selectF: Button=Button(self,text="Load environment", font=TEXT_FONT,command=self._selectSession)
        selectF.grid(row=2,column=0, padx=5)
        makeF: Button=Button(self,text="Create environment", font=TEXT_FONT,command=self._createSession)
        makeF.grid(row=2,column=1, padx=5)
        log.info("GUI init")

    def _selectSession(self) -> None:
        sessionDir:str=filedialog.askdirectory(title='Select session directory').replace("/","\\")
        
        # check if directory was selected
        if sessionDir=="":return

        sessionData.dataStruct.dir=sessionDir
        sessionData.load()
        onload()
        ontomenu()

    def _createSession(self) -> None:
        sessionDir: str=filedialog.askdirectory(title="Select directory of new session").replace("/","\\")
        
        #check if directory was selected
        if sessionDir=="":return
        
        sessionData.dataStruct.dir=sessionDir
        sessionData.sessionSetup()
        sessionData.load()
        oncreate()
        ontomenu()
    