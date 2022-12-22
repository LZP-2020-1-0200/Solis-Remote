from tkinter import Frame, Misc
from tkinterGUIS.mainMenu import sessionManager, referenceManager, setSwitcher
from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Generates a GUI of the main Scene"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        log.debug("GUI init")
        referenceManager.GUI(self).grid(row=0,column=0)
        
        setSwitcher.GUI(self).grid(row=0,column=1)

        sessionManager.GUI(self).grid(row=1,column=0,columnspan=2)
        
    
