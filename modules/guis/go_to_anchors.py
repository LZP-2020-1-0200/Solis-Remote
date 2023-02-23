"""Contains a GUI class for moving the stage to a specific anchor"""
import logging
from tkinter import Frame, Button, Misc
from ..classes.session_data import data_struct
from ..classes import MicroscopeMover, Logger, MicroscopeStatus
from ..helpers.configuration import TEXT_FONT

log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Generates a GUI for moving to Nth point"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        Button(self, text="Go to anchor 1", font=TEXT_FONT,
            command=lambda:self._go_to_anchor(0)
            ).grid(row=0,column=0)

        Button(self, text="Go to anchor 2", font=TEXT_FONT,
            command=lambda:self._go_to_anchor(1)
            ).grid(row=0,column=1)

        Button(self, text="Go to anchor 3", font=TEXT_FONT,
            command=lambda:self._go_to_anchor(2)
            ).grid(row=0,column=2)

    def _go_to_anchor(self, ind:int) -> None:
        with MicroscopeMover() as mover:
            if mover.last_status==MicroscopeStatus.CONNECTED:
                mover.set_coordinates(data_struct.anchors[ind])
