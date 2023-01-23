"""Generates the buttons to go to button and marker setup"""
from tkinter import Button, Frame, Misc
import logging

from ...classes import session_data, Logger, CustomEvent
from ...helpers.configuration import TEXT_FONT

log:logging.Logger=Logger(__name__).get_logger()


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
        session_data.data_struct.onstatuschange.bind(self._update_buttons)
        log.info("GUI init")
        self.onmovetoset:CustomEvent=CustomEvent("set_switcherGUI.onmovetoset")
        self.onmovetoanchor:CustomEvent=CustomEvent("set_switcherGUI.onmovetoanchor")

    def _update_buttons(self) -> None:
        """Updates the state of buttons"""
        assert self._set_points_button is not None and self._set_markers_button is not None
        if session_data.data_struct.points_set:
            self._set_points_button["state"]="disabled"
        else:
            self._set_points_button["state"]="normal"
        if session_data.data_struct.local_anchors_set:
            self._set_markers_button["state"]="disable"
        else:
            self._set_markers_button["state"]="normal"
        log.debug("updated buttons")

    def _set_points(self) -> None:
        self.onmovetoset()

    def _set_anchors(self) -> None:
        self.onmovetoanchor()
