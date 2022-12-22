"""Generates the buttons to go to button and marker setup"""
from classes.event import CustomEvent
from tkinter import Button, Frame, Misc
from helpers.configuration import *
from classes import sessionData
from classes.logger import Logger
import logging

log:logging.Logger=Logger(__name__).get_logger()


onmovetoset:CustomEvent=CustomEvent()
onmovetoset.bind(lambda:log.info("onmovetoset called"))

onmovetoanchor:CustomEvent=CustomEvent()
onmovetoanchor.bind(lambda:log.info("onmovetoanchor called"))

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._set_points_button: Button=Button(self,text="Set points",font=TEXT_FONT,command=self._setPoints)
        self._set_points_button.grid(row=0,column=0)

        self._set_markers_button: Button=Button(self, text="Set anchors",font=TEXT_FONT,command=self._setAnchors)
        self._set_markers_button.grid(row=1,column=0)
        sessionData.onstatuschange.bind(self._updateButtons)
        log.info("GUI init")
    
    def _updateButtons(self) -> None:
        assert self._set_points_button is not None and self._set_markers_button is not None
        if sessionData.dataStruct.points_set:
            self._set_points_button["state"]="disabled"
        else:
            self._set_points_button["state"]="normal"
        if sessionData.dataStruct.local_anchors_set:
            self._set_markers_button["state"]="disable"
        else:
            self._set_markers_button["state"]="normal"
        log.debug("updated buttons")
    
    def _setPoints(self) -> None:
        onmovetoset()

    def _setAnchors(self) -> None:
        onmovetoanchor()
