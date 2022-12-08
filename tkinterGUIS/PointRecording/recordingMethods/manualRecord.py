from tkinter import Button, Frame
from tkinterGUIS  import connection, sessionData
from classes.coordinate import Coordinate
from classes.mover  import mover
from tkinterGUIS.PointRecording import pointRecord
from helpers.configuration import TEXT_FONT


def regPoint() -> None:
    """Adds a point"""
    if connection.getStatus():
        coord:Coordinate=mover.get_coordinates()
        sessionData.add_data_point(coord)

def unregPoint() -> None:
    """Removes the point from memory"""
    sessionData.pop_data_point()


def submit() -> None:
    sessionData.submit_data_points()
    pointRecord.onsubmitpoints()

def generateIn(parentFrame:Frame) -> None:

    Button(parentFrame,text="Add point",command=regPoint,font=TEXT_FONT).grid(row=0,column=0)
    Button(parentFrame, text="Undo last point", command=unregPoint,font=TEXT_FONT).grid(row=0,column=1)
    Button(parentFrame,text="Submit", command=submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)
