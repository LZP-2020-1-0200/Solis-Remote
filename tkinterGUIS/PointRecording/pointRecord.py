from tkinter import IntVar, Frame, Radiobutton, Misc
from classes import sessionData
from tkinterGUIS.PointRecording import pointDisplay, setLoc
from helpers.configuration import TEXT_FONT
from classes.sceneSwitcher import SceneSwitcher
from classes.event import CustomEvent
from tkinterGUIS.PointRecording.recordingMethods import manualRecord, lineRecord, rectangleRecord
from classes.logger import Logger
import logging

log:logging.Logger=Logger(__name__).get_logger()



onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))
oncancelpointselection:CustomEvent=CustomEvent()
oncancelpointselection.bind(lambda:log.info("oncancelpointselection called"))

class GUI(Frame):
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self,parent)
        self._regMethod: IntVar=IntVar()

        mapFrame: Frame=pointDisplay.GUI(self)
        mapFrame.grid(row=0,column=0,columnspan=2)

        relativeMove: Frame=setLoc.GUI(self)
        relativeMove.grid(row=0,column=2,columnspan=2)


        recordingFrame: Frame=Frame(self)
        recordingFrame.grid(row=1, column=1,columnspan=3)
        self._rec_scene_switcher: SceneSwitcher=SceneSwitcher(recordingFrame)

        manual_mode: int=self._rec_scene_switcher.addScene()
        manualRecord.GUI(self._rec_scene_switcher.getFrame(manual_mode)).pack()
        manualRecord.onsubmitpoints.bind(onsubmitpoints)

        line_mode: int=self._rec_scene_switcher.addScene()
        lineRecord.GUI(self._rec_scene_switcher.getFrame(line_mode)).pack()
        lineRecord.onsubmitpoints.bind(onsubmitpoints)

        rectangle_mode: int=self._rec_scene_switcher.addScene()
        rectangleRecord.GUI(self._rec_scene_switcher.getFrame(rectangle_mode)).pack()
        rectangleRecord.onsubmitpoints.bind(onsubmitpoints)

        recordingType: Frame=Frame(self)
        recordingType.grid(row=1,column=0)
        
        Radiobutton(recordingType, text = "Point", variable = self._regMethod, command=self._methodChange,
            value = manual_mode, background = "light blue", font=TEXT_FONT).grid(row=0,column=0,ipady = 5,ipadx=5,sticky="news")
        Radiobutton(recordingType, text = "Line", variable = self._regMethod, command=self._methodChange,
            value = line_mode, background = "light blue", font=TEXT_FONT).grid(row=1,column=0,ipady = 5,ipadx=5,sticky="news")
        Radiobutton(recordingType, text = "Rectangle", variable = self._regMethod, command=self._methodChange,
            value = rectangle_mode, background = "light blue", font=TEXT_FONT).grid(row=2,column=0,ipady = 5,ipadx=5,sticky="news")
        log.info("GUI init")

    def _methodChange(self) -> None:
        if self._rec_scene_switcher is None or self._regMethod is None: return
        self._rec_scene_switcher.switchTo(self._regMethod.get())
        sessionData.clear_data_points()

