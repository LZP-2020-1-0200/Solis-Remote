from tkinter import Button,Frame,Label,StringVar, Misc
from classes import sessionData
from helpers.configuration import *
from tkinterGUIS import connection
from tkinterGUIS.PointRecording import setLoc
from classes.coordinate import Coordinate
from classes.mover import mover
from classes.event import CustomEvent

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

onconfirmanchors:CustomEvent=CustomEvent()
onconfirmanchors.bind(lambda:log.info("onconfirmanchors called"))

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._anchor_coords_vars:list[StringVar]=[StringVar(),StringVar(),StringVar()]
        self._anchor_coords:list[Coordinate|None]=[None, None, None] 
        Label(self,font=TITLE_FONT, text="Anchors").grid(row=0,column=0,columnspan=3)
    
        Button(self, font=TEXT_FONT,command=lambda:self._setAnchor(0), text="Set anchor 1").grid(row=1,column=0)
        Button(self, font=TEXT_FONT,command=lambda:self._setAnchor(1), text="Set anchor 2").grid(row=1,column=1)
        Button(self, font=TEXT_FONT,command=lambda:self._setAnchor(2), text="Set anchor 3").grid(row=1,column=2)

        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[0]).grid(row=2,column=0)
        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[1]).grid(row=2,column=1)
        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[2]).grid(row=2,column=2)

        Button(self, font=TEXT_FONT, command=lambda:self._confirm(), text="Confirm").grid(row=3,column=0,columnspan=3)
        setLoc.GUI(self).grid(row=4,column=0,columnspan=3)
        log.info("GUI init")

    def _confirm(self) -> None:
        # send confirmation event when all coordinates are set
        if self._anchor_coords[0] is not None and self._anchor_coords[1] is not None and self._anchor_coords[2] is not None:
            sessionData.set_local_anchors(self._anchor_coords[0],self._anchor_coords[1],self._anchor_coords[2])
            onconfirmanchors()
    def _setAnchor(self,id:int) -> None:
        if connection.getStatus():
            self._anchor_coords[id]=mover.get_coordinates()
            v:StringVar|None=self._anchor_coords_vars[id]
            coords: Coordinate | None=self._anchor_coords[id]
            if v is not None and coords is not None:
                v.set("X: "+str(coords.x)+"\nY: "+str(coords.y))