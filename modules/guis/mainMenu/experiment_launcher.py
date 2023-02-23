"""Contains GUI and functions for launching experiments"""
import math
import os
from typing import Literal
import logging
from tkinter import Frame, Button, Label, StringVar, Toplevel, Radiobutton, Misc
from ...classes import MicroscopeMover, session_data, CustomEvent, publisher, MicroscopeStatus
from ...helpers import configuration
from ...helpers.configuration import TEXT_FONT

from ...classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

oncapture:CustomEvent=CustomEvent("experiment_launcher.oncapture")

def _run() -> None:
    """Launches an experiment and stores all recorded points in a folder."""
    
    with MicroscopeMover() as mover:
        if mover.last_status==MicroscopeStatus.CONNECTED:
            log.info("Launching experiment")
            #finds the lowest unused experiment number
            i:int=0
            experiment_dir: str=""
            while True:
                experiment_dir=os.path.join(session_data.data_struct.dir,"experiments", str(i).zfill(3))
                if not os.path.isdir(experiment_dir):
                    os.mkdir(experiment_dir)
                    break
                i+=1

            if experiment_dir != "":
                log.info("Experiment directory found")

                #prompt the user for a medium
                medium:str=_prompt_medium()
                if medium!="":
                    #add the experiment to sessionData and close the popup
                    relative_path:str=os.path.relpath(experiment_dir,session_data.data_struct.dir)
                    session_data.add_experiment(relative_path,medium)
                    log.info("Starting experiment")
                    #launch the experiment
                    mover.set_output_directory(experiment_dir)
                    publisher.publish_json("experiment", {
                        "dir":os.path.relpath(os.path.join(session_data.data_struct.dir,"imgs", "experiments", str(i).zfill(3)),"P:\\"),
                        "experiment_number":len(session_data.data_struct.experiments)-1
                    })
                    for ind, point in enumerate(session_data.data_struct.local_points):
                        mover.set_coordinates(point.coordinate)
                        publisher.publish_json("capture", {
                            "experiment_number":len(session_data.data_struct.experiments)-1,
                            "picture_name":point.filename,
                            "dir":os.path.relpath(os.path.join(session_data.data_struct.dir,"imgs", "experiments", str(i).zfill(3)),"P:\\"),
                            "point_number":ind
                            })
                        mover.take_capture(point.filename)
                else:
                    log.info("Environment was not selected")

def _prompt_medium() -> str:
    #Generates an environment popup
    top_level: Toplevel=Toplevel()
    top_level.title("Select an environment")
    experiment_medium: StringVar=StringVar()

    # change the variable to stop blocking if the popup is closed
    top_level.protocol("WM_DELETE_WINDOW", lambda:experiment_medium.set(""))

    #lists all environments in a square
    media: list[str] = configuration.get_media()
    square_size: int=math.ceil(math.sqrt(len(media)))
    for ind, med in enumerate(media):
        Radiobutton(top_level, text = med, variable = experiment_medium, indicatoron=False,
                value = med,
                background = "light blue").grid(
                    row=ind//square_size,
                    column=ind%square_size,
                    ipady = 5,
                    ipadx=5,
                    sticky="news")
    # wait until something is chosen

    top_level.wait_variable(experiment_medium)

    #Confirmation button appears only after an environment has been selected
    var: StringVar = StringVar()
    confirmation_button: Button = Button(
        top_level,
        text="Set",
        command=lambda: var.set("1"))
    confirmation_button.grid(
        row=square_size,
        column=0,
        columnspan=square_size,
        sticky="news",
        ipady=5,
        ipadx = 5)
    confirmation_button.wait_variable(var)
    log.info("Medium selected")

    #close the popup and return
    top_level.destroy()
    return experiment_medium.get()


_CHECK: Literal['✓']="✓"
_CROSS: Literal['✗']="✗"


class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._point_status: StringVar=StringVar()
        self._marker_status: StringVar=StringVar()
        self._local_marker_status: StringVar=StringVar()

        self.start_button: Button = Button(self,
            text="Launch experiment",
            font=TEXT_FONT,
            command=_run)
        self.start_button.grid(row=0,column=1, padx=5,sticky="news")

        checklist: Frame=Frame(self)
        checklist.grid(row=0,column=0)

        #Labels
        Label(checklist, text="Points", font=TEXT_FONT).grid(row=0,column=0)
        Label(checklist, text="Anchors", font=TEXT_FONT).grid(row=1,column=0)
        Label(checklist, text="Local anchors", font=TEXT_FONT).grid(row=2,column=0)

        #status checkmarks
        Label(checklist,textvariable=self._point_status, font=TEXT_FONT).grid(row=0,column=1)
        Label(checklist,textvariable=self._marker_status, font=TEXT_FONT).grid(row=1,column=1)
        Label(checklist,textvariable=self._local_marker_status, font=TEXT_FONT).grid(row=2,column=1)
        self._status_update()
        session_data.data_struct.onstatuschange.bind(self._status_update)
        log.info("GUI init")
    def _status_update(self) -> None:
        """Checks and updates the labels,
        and the launch experiment button according to data flags
        """
        #{"points_set":False,"anchors_set":False}
        if session_data.data_struct.points_set:
            self._point_status.set(_CHECK)
        else:
            self._point_status.set(_CROSS)
        if session_data.data_struct.anchors_set:
            self._marker_status.set(_CHECK)
        else:
            self._marker_status.set(_CROSS)
        if session_data.data_struct.local_anchors_set:
            self._local_marker_status.set(_CHECK)
        else:
            self._local_marker_status.set(_CROSS)
        if (    session_data.data_struct.points_set and
                session_data.data_struct.anchors_set and
                session_data.data_struct.local_anchors_set):
            self.start_button["state"]="normal"
        else:
            self.start_button["state"]="disabled"
        log.info("Updating status")
