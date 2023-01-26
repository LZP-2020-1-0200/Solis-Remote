"""Contains a class that handles reference management"""

import os
import logging
from tkinter import Label, Button, Misc, Frame

from ...helpers.configuration import TITLE_FONT, REFERENCE_NAMES, TEXT_FONT

from ...classes import MicroscopeMover, Logger, session_data
log:logging.Logger=Logger(__name__).get_logger()


class GUI(Frame):
    """Generates a GUI of the Reference measurment"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        label: Label=Label(self, text="References",font=TITLE_FONT)
        label.grid(row=0,column=0,columnspan=2)

        dark_reference_button: Button=Button(self,
            text=REFERENCE_NAMES[0]+" Ref",
            font=TEXT_FONT,
            command=lambda:MicroscopeMover.converse(lambda mover:self._take_reference(mover, 0)))
        dark_reference_button.grid(row=3,column=0, padx=5,sticky="news")

        white_reference_button: Button=Button(self,
            text=REFERENCE_NAMES[1]+ " Ref",
            font=TEXT_FONT,
            command=lambda:MicroscopeMover.converse(lambda mover:self._take_reference(mover, 1)))
        white_reference_button.grid(row=3,column=1, padx=5,sticky="news")

        dark_for_white_ref_button: Button=Button(self,
            text=REFERENCE_NAMES[2]+ " Ref",
            font=TEXT_FONT,
            command=lambda:MicroscopeMover.converse(lambda mover:self._take_reference(mover, 2)))
        dark_for_white_ref_button.grid(row=4,column=0,columnspan=2, padx=5,sticky="news")
        log.debug("GUI init")

    def _take_reference(self,mover:MicroscopeMover, reference_type:int) -> None:
        """Runs a capture and stores it as a reference"""
        log.info("Taking reference")
        log.info("Prompt for SOLIS")
        i:int=1
        full_dir:str=""
        rel_dir:str=""
        filename:str=""
        log.debug("Finding free reference name")
        while True:
            filename=REFERENCE_NAMES[reference_type]+str(i).zfill(2)+".asc"
            rel_dir=os.path.join("refs",filename)
            full_dir=os.path.join(session_data.data_struct.dir,rel_dir)
            if not os.path.isfile(full_dir):
                break
            i+=1
        log.debug("Reference name %s found", filename)
        session_data.add_reference(rel_dir,REFERENCE_NAMES[reference_type])
        mover.set_output_directory(os.path.join(session_data.data_struct.dir,"refs"))
        log.info("Starting spectrogram")
        mover.take_capture(filename)
        log.info("Finished spectrogram")
