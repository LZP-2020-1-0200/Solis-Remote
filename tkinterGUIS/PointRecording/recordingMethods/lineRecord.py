from tkinterGUIS  import connection
from tkinterGUIS  import sessionData
from tkinterGUIS.PointRecording import pointRecord
from helpers.configuration import TEXT_FONT
from classes.mover  import mover
from classes.coordinate import Coordinate
from tkinter import StringVar, Frame,Button,Label,Entry


pointCoords:list[Coordinate]=[]

pointCounter:StringVar|None=None

ptCount:int=0

def counterUpdate(strVar:StringVar|None) -> None:
    """Gets the number from the number of points entry and recalculates all points"""
    global ptCount
    if strVar is None: return
    t: str=strVar.get()
    if t.isnumeric():
        ptCount=int(t)
    print(ptCount)
    recalculate()

def recalculate() -> None:
    """recalculates the intermediary points and refreshes pointDisplay"""
    totalCoords:list[Coordinate]=[]
    for ind,pt in enumerate(pointCoords[:-1]):
        other: Coordinate=pointCoords[ind+1]
        totalCoords.append(pt)
        step: Coordinate=(other-pt)/(ptCount-1)
        for ind in range(ptCount-2):
            totalCoords.append((pt+(step*(ind+1))).rounded())
    totalCoords.append(pointCoords[-1].rounded())
    sessionData.clear_data_points()
    sessionData.add_data_points(totalCoords)


def regPoint() -> None:
    """Adds the current stage position and recalculates points"""
    if connection.getStatus():
        coord:Coordinate
        coord=mover.get_coordinates()
        pointCoords.append(coord)
        recalculate()

def unregPoint() -> None:
    """Removes the last coordinate and recalculates points"""
    pointCoords.pop()
    recalculate()

def submit() -> None:
    recalculate()
    sessionData.submit_data_points()
    pointRecord.onsubmitpoints()


def generateIn(parentFrame:Frame) -> None:
    global pointCounter
    pointCounter=StringVar()
    Button(parentFrame,text="Add point",command=regPoint,font=TEXT_FONT).grid(row=0,column=0)
    Button(parentFrame, text="Undo last point", command=unregPoint,font=TEXT_FONT).grid(row=0,column=1)
    Button(parentFrame,text="Submit", command=submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)
    Label(parentFrame,text="Enter amount of points").grid(row=2,column=0, padx=5)
    Entry(parentFrame,textvariable=pointCounter).grid(row=2,column=1, padx=5)
    pointCounter.trace_add("write", lambda a,b,c: counterUpdate(pointCounter))

