
from tkinter import * 
import classes.mover
import classes.coordinate
from collections.abc import Callable
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
from tkinter import messagebox

status=False
def getStatus():
    if not status: 
        messagebox.showinfo("","SolisXY GUI is not connected to SOLIS")
    return status
def generateIn(parentFrame,mover):
    title=Label(parentFrame,text="Point registration",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)
    statusLabel=Label(parentFrame,text="Disconnected.",font=TEXT_FONT)
    statusLabel.grid(row=1,column=0,columnspan=2)

    def connect():
        if not messagebox.askyesno("","Is SOLIS script on?"):
            return
        global status
        if mover.connect("COM6"):
            statusLabel.config(text="Connected to COM6.")
            #mover.set_coordinates(classes.coordinate.Coordinate(8000,-8000))
            status=True
        else:
            statusLabel.config(text="Connection failed.")
            status=False
        print(f"Connection status: {getStatus()}")

    def disconnect():
        global status
        mover.close_connection()
        statusLabel.config(text="Connection closed.")
        status=False


    connectB = Button(parentFrame,text="Connect", font=TEXT_FONT, command=connect)
    connectB.grid(row=2,column=0, padx=5)

    disconnectB = Button(parentFrame,text="Disconnect", font=TEXT_FONT, command=disconnect)
    disconnectB.grid(row=2,column=1,padx=5)

