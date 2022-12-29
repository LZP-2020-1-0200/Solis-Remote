"""Contains main scene GUI class"""
from tkinter import Frame, Misc
import logging
from . import experiment_launcher, reference_manager, set_switcher
from ...classes.logger import Logger
log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Generates a GUI of the main Scene"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        log.debug("GUI init")
        reference_manager.GUI(self).grid(row=0,column=0)

        set_switcher.GUI(self).grid(row=0,column=1)

        experiment_launcher.GUI(self).grid(row=1,column=0,columnspan=2)
