"""Generates the buttons to go to button and marker setup"""
from tkinter import Button, Frame, Misc
import logging

from ...classes.event import CustomEvent
from ...helpers.configuration import TEXT_FONT
from ...classes import session_data
from ...classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()


onmovetoset:CustomEvent=CustomEvent()
onmovetoset.bind(lambda:log.info("onmovetoset called"))

onmovetoanchor:CustomEvent=CustomEvent()
onmovetoanchor.bind(lambda:log.info("onmovetoanchor called"))

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._set_points_button: Button=Button(
            self,
            text="Set points",
            font=TEXT_FONT,
            command=self._set_points)
        self._set_points_button.grid(row=0,column=0)

        self._set_markers_button: Button=Button(
            self,
            text="Set anchors",
            font=TEXT_FONT,
            command=self._set_anchors)
        self._set_markers_button.grid(row=1,column=0)
        session_data.onstatuschange.bind(self._update_buttons)
        log.info("GUI init")

    def _update_buttons(self) -> None:
        """Updates the state of buttons"""
        assert self._set_points_button is not None and self._set_markers_button is not None
        if session_data.dataStruct.points_set:
            self._set_points_button["state"]="disabled"
        else:
            self._set_points_button["state"]="normal"
        if session_data.dataStruct.local_anchors_set:
            self._set_markers_button["state"]="disable"
        else:
            self._set_markers_button["state"]="normal"
        log.debug("updated buttons")

    def _set_points(self) -> None:
        onmovetoset()

    def _set_anchors(self) -> None:
        onmovetoanchor()
