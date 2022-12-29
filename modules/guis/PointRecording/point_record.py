"""Contains a GUI class that contains the display and the various recording methods"""
import logging
from tkinter import IntVar, Frame, Radiobutton, Misc

from . import point_display, set_loc
from .recordingMethods import manual_record, line_record, rectangle_record
from ...classes import session_data
from ...classes.scene_switcher import SceneSwitcher
from ...classes.event import CustomEvent
from ...classes.logger import Logger
from ...helpers.configuration import TEXT_FONT
log:logging.Logger=Logger(__name__).get_logger()



onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))
oncancelpointselection:CustomEvent=CustomEvent()
oncancelpointselection.bind(lambda:log.info("oncancelpointselection called"))

class GUI(Frame):
    """Generates a GUI containing recording GUIs, a display GUI and relative movement GUI"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self,parent)
        self._reg_method_var: IntVar=IntVar()

        map_frame: Frame=point_display.GUI(self)
        map_frame.grid(row=0,column=0,columnspan=2)

        relative_move_frame: Frame=set_loc.GUI(self)
        relative_move_frame.grid(row=0,column=2,columnspan=2)


        recording_frame: Frame=Frame(self)
        recording_frame.grid(row=1, column=1,columnspan=3)
        self._rec_scene_switcher: SceneSwitcher=SceneSwitcher(recording_frame)

        manual_mode: int=self._rec_scene_switcher.add_scene()
        manual_record.GUI(self._rec_scene_switcher.get_frame(manual_mode)).pack()
        manual_record.onsubmitpoints.bind(onsubmitpoints)

        line_mode: int=self._rec_scene_switcher.add_scene()
        line_record.GUI(self._rec_scene_switcher.get_frame(line_mode)).pack()
        line_record.onsubmitpoints.bind(onsubmitpoints)

        rectangle_mode: int=self._rec_scene_switcher.add_scene()
        rectangle_record.GUI(self._rec_scene_switcher.get_frame(rectangle_mode)).pack()
        rectangle_record.onsubmitpoints.bind(onsubmitpoints)

        recording_type: Frame=Frame(self)
        recording_type.grid(row=1,column=0)

        Radiobutton(recording_type,
            text = "Point",
            variable = self._reg_method_var,
            command=self._method_change,
            value = manual_mode,
            background = "light blue",
            font=TEXT_FONT
            ).grid(row=0,column=0,ipady = 5,ipadx=5,sticky="news")
        Radiobutton(recording_type,
            text = "Line",
            variable = self._reg_method_var,
            command=self._method_change,
            value = line_mode,
            background = "light blue",
            font=TEXT_FONT
            ).grid(row=1,column=0,ipady = 5,ipadx=5,sticky="news")
        Radiobutton(recording_type,
            text = "Rectangle",
            variable = self._reg_method_var,
            command=self._method_change,
            value = rectangle_mode,
            background = "light blue",
            font=TEXT_FONT
            ).grid(row=2,column=0,ipady = 5,ipadx=5,sticky="news")
        log.info("GUI init")

    def _method_change(self) -> None:
        if self._rec_scene_switcher is None or self._reg_method_var is None:
            return
        self._rec_scene_switcher.switch_to(self._reg_method_var.get())
        session_data.clear_data_points()
