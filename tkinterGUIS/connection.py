
from tkinter import Frame, Label, Button, Misc
from classes.mover import mover, MicroscopeStatus
from helpers.configuration import TEXT_FONT
from tkinter import messagebox
from classes.event import CustomEvent

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

onconnect:CustomEvent=CustomEvent()
onconnect.bind(lambda:log.info("onconnect called"))
def getStatus()->bool:
    """
    Wrapper function that informs the user if connection to SOLIS has not yet been established
    """
    log.info("Getting microscope mover status")
    status: MicroscopeStatus=mover.ping()
    if status==MicroscopeStatus.DISCONNECTED:
        messagebox.showwarning("Warning","SolisXY GUI is not connected to SOLIS")#type: ignore
        return False
    if status==MicroscopeStatus.SOLIS_UNRESPONSIVE:
        messagebox.showwarning("Ping failed", "SOLIS script did not respond.")#type: ignore
        return False
    if status==MicroscopeStatus.STAGE_UNRESPONSIVE:
        messagebox.showwarning("Ping failed", #type: ignore
            "SOLIS script was responsive,\n"+
            "but the stage did not respond.\n"+
            "Please check if the stage controller is on and connected,\n"+
            "and restart the SOLIS script.")
        return False
    return True

class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        title: Label=Label(self,text="Connection to SOLIS",font=TEXT_FONT)
        title.grid(row=0,column=0,columnspan=2)
        self.statusLabel: Label=Label(self,text="Disconnected.",font=TEXT_FONT)
        self.statusLabel.grid(row=1,column=0,columnspan=2)

       

        connectB: Button = Button(self,text="Connect", font=TEXT_FONT, command=self._connect)
        connectB.grid(row=2,column=0, padx=5)

        disconnectB: Button = Button(self,text="Disconnect", font=TEXT_FONT, command=self._disconnect)
        disconnectB.grid(row=2,column=1,padx=5)
        log.info("GUI init")
    
    def _disconnect(self) -> None:
        """
        Wrapper function for informing the user about disconnecting
        """
        
        mover.close_connection()
        self.statusLabel.config(text="Connection closed.")

    def _connect(self) -> None:
            """
            Wrapper function for informing the user about the connection status
            """
            if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
                return
            mover.connect("COM6")
            if getStatus():
                self.statusLabel.config(text="Connected to COM6.")
                onconnect()
            else:
                self.statusLabel.config(text="Connection failed.")
    