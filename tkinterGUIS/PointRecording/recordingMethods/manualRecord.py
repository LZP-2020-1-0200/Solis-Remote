from tkinter import Button, Frame, Misc
from classes import sessionData
from tkinterGUIS  import connection
from classes.coordinate import Coordinate
from classes.mover  import mover
from classes.event import CustomEvent
from helpers.configuration import TEXT_FONT

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))

class GUI(Frame):
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self,parent)
        Button(self,text="Add point",command=self._regPoint,font=TEXT_FONT).grid(row=0,column=0)
        Button(self, text="Undo last point", command=self._unregPoint,font=TEXT_FONT).grid(row=0,column=1)
        Button(self,text="Submit", command=self._submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)
        log.info("GUI init")

    def _regPoint(self) -> None:
        """Adds a point"""
        if connection.getStatus():
            coord:Coordinate=mover.get_coordinates()
            sessionData.add_data_point(coord)

    def _unregPoint(self) -> None:
        """Removes the point from memory"""
        sessionData.pop_data_point()


    def _submit(self) -> None:
        sessionData.submit_data_points()
        onsubmitpoints()

