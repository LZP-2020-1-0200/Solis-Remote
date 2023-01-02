"""Contains the GUI for anchors """
from tkinter import Button,Frame,Label,StringVar, Misc
import logging

from ..helpers.configuration import TEXT_FONT, TITLE_FONT

from ..guis import connection
from ..guis.PointRecording import set_loc

from ..classes import session_data
from ..classes.coordinate import Coordinate
from ..classes.mover import mover
from ..classes.event import CustomEvent
from ..classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._anchor_coords_vars:list[StringVar]=[StringVar(),StringVar(),StringVar()]
        self._anchor_coords:list[Coordinate|None]=[None, None, None]
        Label(self,font=TITLE_FONT, text="Anchors").grid(row=0,column=0,columnspan=3)

        Button(self, font=TEXT_FONT,
            command=lambda:self._set_anchor(0), text="Set anchor 1").grid(row=1,column=0)
        Button(self, font=TEXT_FONT,
            command=lambda:self._set_anchor(1), text="Set anchor 2").grid(row=1,column=1)
        Button(self, font=TEXT_FONT,
            command=lambda:self._set_anchor(2), text="Set anchor 3").grid(row=1,column=2)

        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[0]).grid(row=2,column=0)
        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[1]).grid(row=2,column=1)
        Label(self, font=TEXT_FONT, textvariable=self._anchor_coords_vars[2]).grid(row=2,column=2)

        self.onconfirmanchors:CustomEvent=CustomEvent("AnchorsGUI.onconfirmanchors")
        self.oncancelanchors:CustomEvent=CustomEvent("AnchorsGUI.cancelanchors")

        Button(self, font=TEXT_FONT,
            command=self._confirm, text="Confirm").grid(row=3,column=0,columnspan=3)
        Button(self, font=TEXT_FONT,
            command=self.oncancelanchors, text="Go back").grid(row=5,column=0)
        set_loc.GUI(self).grid(row=4,column=0,columnspan=3)
        log.info("GUI init")


    def _confirm(self) -> None:
        # send confirmation event when all coordinates are set
        if (
                self._anchor_coords[0] is not None and
                self._anchor_coords[1] is not None and
                self._anchor_coords[2] is not None
            ):
            session_data.set_local_anchors(
                self._anchor_coords[0],
                self._anchor_coords[1],
                self._anchor_coords[2])
            log.info("Anchors set")
            self.onconfirmanchors()

    def _set_anchor(self,index:int) -> None:
        if connection.get_status():
            self._anchor_coords[index]=mover.get_coordinates()
            coords: Coordinate | None=self._anchor_coords[index]
            str_var:StringVar=self._anchor_coords_vars[index]
            if coords is not None:
                str_var.set("X: "+str(coords.x)+"\nY: "+str(coords.y))
            log.info("Anchor %i set", index)
                