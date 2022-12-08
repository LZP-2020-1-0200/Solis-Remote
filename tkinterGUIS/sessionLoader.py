from classes.event import CustomEvent
from tkinter import Button, filedialog, Frame
from helpers.configuration import *
from tkinterGUIS import sessionData

onload:CustomEvent=CustomEvent()
oncreate:CustomEvent=CustomEvent()
onToMenu:CustomEvent=CustomEvent()



def selectSession() -> None:
    global onload
    sessionData.dataStruct.dir=filedialog.askdirectory(title='Select session directory').replace("/","\\")
    sessionData.load()
    onload()
    onToMenu()



def createSession() -> None:
    global dir
    sessionData.dataStruct.dir=filedialog.askdirectory(title="Select directory of new session").replace("/","\\")
    sessionData.sessionSetup()
    sessionData.load()
    oncreate()
    onToMenu()


def generateIn(parentFrame:Frame) -> None:
    selectF: Button=Button(parentFrame,text="Load environment", font=TEXT_FONT,command=selectSession)
    selectF.grid(row=2,column=0, padx=5)
    makeF: Button=Button(parentFrame,text="Create environment", font=TEXT_FONT,command=createSession)
    makeF.grid(row=2,column=1, padx=5)