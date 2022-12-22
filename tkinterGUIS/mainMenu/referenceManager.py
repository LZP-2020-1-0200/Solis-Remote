from tkinter import Label, Button, Misc, Frame, messagebox
from classes import sessionData

from helpers.configuration import *

from tkinterGUIS import connection
from classes.mover import mover
import os

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()



class GUI(Frame):
    """Generates a GUI of the Reference measurment"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        label: Label=Label(self, text="References",font=TITLE_FONT)
        label.grid(row=0,column=0,columnspan=2)

        refD: Button=Button(self,text=referenceNames[0]+" Ref", font=TEXT_FONT, command=lambda:self._takeReference(0))
        refD.grid(row=3,column=0, padx=5,sticky="news")

        refB: Button=Button(self,text=referenceNames[1]+ " Ref", font=TEXT_FONT, command=lambda:self._takeReference(1))
        refB.grid(row=3,column=1, padx=5,sticky="news")

        refDB: Button=Button(self,text=referenceNames[2]+ " Ref", font=TEXT_FONT, command=lambda:self._takeReference(2))
        refDB.grid(row=4,column=0,columnspan=2, padx=5,sticky="news")
        log.debug("GUI init")

    def _takeReference(self, referenceType:int) -> None:
        log.info("Taking reference")
        log.info("Prompt for SOLIS")
        if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
            log.info("User denied prompt")
            return
        if connection.getStatus():
            i:int=1
            fullDir:str=""
            relDir:str=""
            filename:str=""
            log.debug("Finding free reference name")
            while True:
                filename=referenceNames[referenceType]+str(i).zfill(2)+".asc"
                relDir=os.path.join("refs",filename)
                fullDir=os.path.join(sessionData.dataStruct.dir,relDir)
                if not os.path.isfile(fullDir):
                    break
                i+=1
            log.debug(f"Reference name {filename} found")
            sessionData.add_reference(relDir,referenceNames[referenceType])
            mover.set_output_directory(os.path.join(sessionData.dataStruct.dir,"refs"))
            log.info("Starting spectrogram")
            mover.take_capture(filename)
            log.info("Finished spectrogram")

