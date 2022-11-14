from tkinter import * 
from collections.abc import Callable
from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
from classes.mover  import mover


def regPoint():
    if connection.status:
        coord=mover.get_coordinates()
        sessionManager.pointList.append((coord.x,coord.y))
        pointDisplay.displayPoints(sessionManager.pointList)
    pass
def unregPoint():
    sessionManager.pointList.pop()
    pointDisplay.displayPoints(sessionManager.pointList)
    pass

parent:Frame=None

def generateIn(parentFrame):
    global parent
    parent=parentFrame
    title=Label(parentFrame,text="Point registration",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    registerButton = Button(parentFrame,text="Register point", font=TEXT_FONT, command=regPoint)
    registerButton.grid(row=1,column=0, padx=5)

    undoButton = Button(parentFrame,text="Undo last point", font=TEXT_FONT, command=unregPoint)
    undoButton.grid(row=1,column=1,padx=5)

