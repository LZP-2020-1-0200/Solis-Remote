
from tkinter import * 
from classes.mover import mover
from collections.abc import Callable
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
from tkinter import messagebox



def getStatus()->bool:
    """
    Wrapper function that informs the user if connection to SOLIS has not yet been established
    """
    status=mover.get_connection_state()
    if not status: 
        messagebox.showwarning("Warning","SolisXY GUI is not connected to SOLIS")
    return status
def generateIn(parentFrame):
    """Generates the connection GUI inside `parentFrame`"""
    
    title=Label(parentFrame,text="Connection to SOLIS",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)
    statusLabel=Label(parentFrame,text="Disconnected.",font=TEXT_FONT)
    statusLabel.grid(row=1,column=0,columnspan=2)

    def connect():
        """
        Wrapper function for informing the user about the connection status
        """

        if not messagebox.askyesno("","Is SOLIS script on?"):
            return
        if mover.connect("COM6"):
            statusLabel.config(text="Connected to COM6.")
        else:
            statusLabel.config(text="Connection failed.")
        

    def disconnect():
        """
        Wrapper function for informing the user about disconnecting
        """
        mover.close_connection()
        statusLabel.config(text="Connection closed.")


    connectB = Button(parentFrame,text="Connect", font=TEXT_FONT, command=connect)
    connectB.grid(row=2,column=0, padx=5)

    disconnectB = Button(parentFrame,text="Disconnect", font=TEXT_FONT, command=disconnect)
    disconnectB.grid(row=2,column=1,padx=5)

