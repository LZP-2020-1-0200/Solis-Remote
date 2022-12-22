from tkinter import Frame, Button, Label, StringVar, Toplevel, messagebox, Radiobutton, Misc
from classes.mover import mover
from tkinterGUIS import connection
from classes import sessionData
from helpers import configuration
from classes import sessionData
from helpers.configuration import TEXT_FONT
import math
import os
from typing import Literal


from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()





def run() -> None:
    log.info("Launching experiment")
    if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
        log.info("User cancelled: SOLIS is off")
        return
    if connection.getStatus():
        #finds the lowest unused experiment number
        i:int=0
        experimentDir: str=""
        while True:
            experimentDir=os.path.join(sessionData.dataStruct.dir,"experiments", str(i).zfill(3) )
            if not os.path.isdir(experimentDir):
                os.mkdir(experimentDir)
                break
            i+=1

        if experimentDir is not None:
            log.info("Experiment directory found")

            #Generates an environment popup
            tp: Toplevel=Toplevel()
            tp.title("Select an environment")
            experimentMedium: StringVar=StringVar()
            #lists all environments in a square
            s: int=math.ceil(math.sqrt(len(configuration.media)))
            for ind, med in enumerate(configuration.media):
                Radiobutton(tp, text = med, variable = experimentMedium, indicatoron=False,
                        value = med,
                        background = "light blue").grid(row=ind//s,column=ind%s,ipady = 5,ipadx=5,sticky="news")
            tp.wait_variable(experimentMedium)
            #Confirmation button appears only after an environment has been selected
            var: StringVar = StringVar()
            button: Button = Button(tp, text="Set", command=lambda: var.set("1"))
            button.grid(row=s,column=0,columnspan=s,sticky="news",ipady=5, ipadx = 5)
            button.wait_variable(var)
            log.info("Medium selected")
            #add the experiment to sessionData and close the popup
            sessionData.add_experiment(os.path.relpath(experimentDir,sessionData.dataStruct.dir),experimentMedium.get())
            tp.destroy()
            log.info("Starting experiment")
            #launch the experiment
            mover.set_output_directory(experimentDir)
            for pt in sessionData.dataStruct.local_points:
                mover.set_coordinates(pt.coordinate)
                mover.take_capture(pt.filename)

_CHECK: Literal['✓']="✓"
_CROSS: Literal['✗']="✗"


class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._point_status: StringVar=StringVar()
        self._marker_status: StringVar=StringVar()
        self._local_marker_status: StringVar=StringVar()
        

        self.startB: Button = Button(self, text="Launch experiment", font=TEXT_FONT, command=run)
        self.startB.grid(row=0,column=1, padx=5,sticky="news")

        checklist: Frame=Frame(self)
        checklist.grid(row=0,column=0)

        Label(checklist, text="Points", font=TEXT_FONT).grid(row=0,column=0)

        Label(checklist, text="Anchors", font=TEXT_FONT).grid(row=1,column=0)

        Label(checklist, text="Local anchors", font=TEXT_FONT).grid(row=2,column=0)

        Label(checklist,textvariable=self._point_status, font=TEXT_FONT).grid(row=0,column=1)

        Label(checklist,textvariable=self._marker_status, font=TEXT_FONT).grid(row=1,column=1)

        Label(checklist,textvariable=self._local_marker_status, font=TEXT_FONT).grid(row=2,column=1)
        self._statusUpdate()
        sessionData.onstatuschange.bind(self._statusUpdate)
        log.info("GUI init")
    def _statusUpdate(self) -> None:
        #{"points_set":False,"anchors_set":False}
        if sessionData.dataStruct.points_set:
            self._point_status.set(_CHECK)
        else:
            self._point_status.set(_CROSS)
        if sessionData.dataStruct.anchors_set:
            self._marker_status.set(_CHECK)
        else:
            self._marker_status.set(_CROSS)
        if sessionData.dataStruct.local_anchors_set:
            self._local_marker_status.set(_CHECK)
        else:
            self._local_marker_status.set(_CROSS)
        if sessionData.dataStruct.points_set and sessionData.dataStruct.anchors_set and sessionData.dataStruct.local_anchors_set:
            self.startB["state"]="normal"
        else:
            self.startB["state"]="disabled"
        log.info("updating status")

