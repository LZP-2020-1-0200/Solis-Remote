"""Contains a GUI class for manual recording."""
import logging
from tkinter import Button, Frame, Misc

from ....guis  import connection
from ....classes import session_data
from ....classes.coordinate import Coordinate
from ....classes.mover  import mover
from ....classes.event import CustomEvent
from ....classes.logger import Logger
from ....helpers.configuration import TEXT_FONT

log:logging.Logger=Logger(__name__).get_logger()


class GUI(Frame):
    """Generates a GUI for recording single points"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self,parent)

        self.onsubmitpoints:CustomEvent=CustomEvent("manual_recordGUI.onsubmitpoints")

        Button(self,text="Add point",command=self._reg_point,font=TEXT_FONT).grid(row=0,column=0)
        Button(self,
            text="Undo last point",
            command=self._unreg_point,
            font=TEXT_FONT
            ).grid(row=0,column=1)
        Button(self,
            text="Submit",
            command=self._submit,
            font=TEXT_FONT
            ).grid(row=1,column=0,columnspan=2)
        log.info("GUI init")

    def _reg_point(self) -> None:
        """Adds a point"""
        if connection.get_status():
            coord:Coordinate=mover.get_coordinates()
            session_data.add_data_point(coord)

    def _unreg_point(self) -> None:
        """Removes the point from memory"""
        session_data.pop_data_point()


    def _submit(self) -> None:
        session_data.submit_data_points()
        self.onsubmitpoints()
