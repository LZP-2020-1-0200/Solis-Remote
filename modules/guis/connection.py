"""Handles informing the user about connections,
serves as a bridge between the user and the `mover`
"""

from tkinter import Frame, Label, Button, Misc, messagebox
import logging

from ..helpers.configuration import TEXT_FONT, LOOPBACK_A

from ..classes.mover import mover, MicroscopeStatus
from ..classes.event import CustomEvent
from ..classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

def get_status()->bool:
    """
    Wrapper function that informs the user if connection to SOLIS has not yet been established
    """
    log.info("Getting microscope mover status")
    status: MicroscopeStatus=mover.ping()
    if status==MicroscopeStatus.DISCONNECTED:
        messagebox.showwarning("Warning","SolisXY GUI is not connected to SOLIS")#type: ignore
        log.info("Not connected to SOLIS.")
        return False
    if status==MicroscopeStatus.SOLIS_UNRESPONSIVE:
        messagebox.showwarning("Ping failed", "SOLIS script did not respond.")#type: ignore
        log.info("SOLIS did not respond.")
        return False
    if status==MicroscopeStatus.STAGE_UNRESPONSIVE:
        messagebox.showwarning("Ping failed", #type: ignore
            "SOLIS script was responsive,\n"+
            "but the stage did not respond.\n"+
            "Please check if the stage controller is on and connected,\n"+
            "and restart the SOLIS script.")
        log.info("SOLIS responsive, Stage unresponsive.")
        return False
    log.info("Ping successful.")
    return True

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        title: Label=Label(self,text="Connection to SOLIS",font=TEXT_FONT)
        title.grid(row=0,column=0,columnspan=2)
        self.status_label: Label=Label(self,text="Disconnected.",font=TEXT_FONT)
        self.status_label.grid(row=1,column=0,columnspan=2)

        connect_button: Button = Button(self,text="Connect", font=TEXT_FONT, command=self._connect)
        connect_button.grid(row=2,column=0, padx=5)

        disconnect_button: Button = Button(
            self,
            text="Disconnect",
            font=TEXT_FONT,
            command=self._disconnect)
        disconnect_button.grid(row=2,column=1,padx=5)
        log.info("GUI init")

        self.onconnect: CustomEvent=CustomEvent("connectionGUI.onconnect")

    def _disconnect(self) -> None:
        """
        Wrapper function for informing the user about disconnecting
        """

        mover.close_connection()
        self.status_label.config(text="Connection closed.")

    def _connect(self) -> None:
        """
        Wrapper function for informing the user about the connection status
        """
        if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
            return
        mover.connect(LOOPBACK_A)
        if get_status():
            self.status_label.config(text=f"Connected to {LOOPBACK_A}.")
            log.info("Connection successful")
            self.onconnect()
        else:
            self.status_label.config(text="Connection failed.")
            log.info("Connection failed")
    