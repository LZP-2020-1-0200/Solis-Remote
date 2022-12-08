
from tkinter import Frame, Label, Button
from classes.mover import mover
from helpers.configuration import TEXT_FONT
from tkinter import messagebox
from classes.event import CustomEvent

onconnect:CustomEvent=CustomEvent()

def getStatus()->bool:
    """
    Wrapper function that informs the user if connection to SOLIS has not yet been established
    """
    status: bool=mover.get_connection_state()
    if not status: 
        messagebox.showwarning("Warning","SolisXY GUI is not connected to SOLIS")#type: ignore
    return status
def generateIn(parentFrame:Frame) -> None:
    """Generates the connection GUI inside `parentFrame`"""
    
    title: Label=Label(parentFrame,text="Connection to SOLIS",font=TEXT_FONT)
    title.grid(row=0,column=0,columnspan=2)
    statusLabel: Label=Label(parentFrame,text="Disconnected.",font=TEXT_FONT)
    statusLabel.grid(row=1,column=0,columnspan=2)

    def connect() -> None:
        """
        Wrapper function for informing the user about the connection status
        """

        if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
            return
        if mover.connect("COM6"):
            statusLabel.config(text="Connected to COM6.")
            onconnect()
        else:
            statusLabel.config(text="Connection failed.")
        

    def disconnect() -> None:
        """
        Wrapper function for informing the user about disconnecting
        """
        
        mover.close_connection()
        statusLabel.config(text="Connection closed.")


    connectB: Button = Button(parentFrame,text="Connect", font=TEXT_FONT, command=connect)
    connectB.grid(row=2,column=0, padx=5)

    disconnectB: Button = Button(parentFrame,text="Disconnect", font=TEXT_FONT, command=disconnect)
    disconnectB.grid(row=2,column=1,padx=5)

