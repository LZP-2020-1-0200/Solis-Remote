from tkinter import IntVar, Frame, Radiobutton
from tkinterGUIS import sessionData
from tkinterGUIS.PointRecording import pointDisplay, setLoc
from helpers.configuration import TEXT_FONT
from classes.sceneSwitcher import SceneSwitcher
from classes.event import CustomEvent
from tkinterGUIS.PointRecording.recordingMethods import manualRecord, lineRecord, rectangleRecord

regMethod:IntVar|None=None


onsubmitpoints:CustomEvent=CustomEvent()

_rec_scene_switcher:SceneSwitcher|None=None

def methodChange() -> None:
    if _rec_scene_switcher is None or regMethod is None: return
    _rec_scene_switcher.switchTo(regMethod.get())
    sessionData.clear_data_points()



def generateIn(parentFrame:Frame) -> None:
    """Generates the point recording GUI inside `parentFrame`"""

    global regMethod, _rec_scene_switcher
    regMethod=IntVar()

    mapFrame: Frame=Frame(parentFrame)
    mapFrame.grid(row=0,column=0,columnspan=2)
    pointDisplay.generateIn(mapFrame)

    relativeMove: Frame=Frame(parentFrame)
    relativeMove.grid(row=0,column=2,columnspan=2)
    setLoc.generateIn(relativeMove)

    recordingType: Frame=Frame(parentFrame)
    recordingType.grid(row=1,column=0)

    recordingFrame: Frame=Frame(parentFrame)
    recordingFrame.grid(row=1, column=1,columnspan=3)
    _rec_scene_switcher=SceneSwitcher(recordingFrame)

    manual_mode: int=_rec_scene_switcher.addScene()
    manualRecord.generateIn(_rec_scene_switcher.getFrame(manual_mode))

    line_mode: int=_rec_scene_switcher.addScene()
    lineRecord.generateIn(_rec_scene_switcher.getFrame(line_mode))

    rectangle_mode: int=_rec_scene_switcher.addScene()
    rectangleRecord.generateIn(_rec_scene_switcher.getFrame(rectangle_mode))


    
    Radiobutton(recordingType, text = "Point", variable = regMethod, command=methodChange,
        value = manual_mode, background = "light blue", font=TEXT_FONT).grid(row=0,column=0,ipady = 5,ipadx=5,sticky="news")
    Radiobutton(recordingType, text = "Line", variable = regMethod, command=methodChange,
        value = line_mode, background = "light blue", font=TEXT_FONT).grid(row=1,column=0,ipady = 5,ipadx=5,sticky="news")
    Radiobutton(recordingType, text = "Rectangle", variable = regMethod, command=methodChange,
        value = rectangle_mode, background = "light blue", font=TEXT_FONT).grid(row=2,column=0,ipady = 5,ipadx=5,sticky="news")



