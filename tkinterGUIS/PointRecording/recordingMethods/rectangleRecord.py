from tkinterGUIS  import connection
from tkinterGUIS  import sessionData
from tkinterGUIS.PointRecording import pointRecord
from helpers.configuration import TEXT_FONT
from classes.mover  import mover
from classes.coordinate import Coordinate
from tkinter import Button, Label, StringVar, Frame, Entry


pointCoords:list[Coordinate]=[]

rowCounter:StringVar|None=None
colCounter:StringVar|None=None

rCount:int=2
cCount:int=2

points:list[Coordinate|None]=[None,None,None]

def regPoint(ind:int) -> None:
    if connection.getStatus():
        points[ind]=mover.get_coordinates()
        recalculate()

def rcounterUpdate(strVar:StringVar|None) -> None:
    """Gets the number from the number of points entry and recalculates all points"""
    global rCount
    if strVar is None: 
        rCount=2
        return
    t: str=strVar.get()
    if t.isnumeric():
        rCount=int(t)
    rCount=max(2,rCount)
    print(rCount)
    recalculate()

def ccounterUpdate(strVar:StringVar|None) -> None:
    """Gets the number from the number of points entry and recalculates all points"""
    global cCount
    if strVar is None: 
        cCount=2
        return
    t: str=strVar.get()
    if t.isnumeric():
        cCount=int(t)
    cCount=max(2,cCount)
    print(cCount)
    recalculate()

def recalculate() -> None:
    """recalculates the intermediary points and refreshes pointDisplay"""
    assert rCount>=2 and cCount>=2
    startingCorner:Coordinate|None=points[0]
    pB:Coordinate|None=points[1]
    pC:Coordinate|None=points[2]
    if startingCorner is None or pB is None or pC is None: return
    vectorX:Coordinate=pB-startingCorner
    vectorAC:Coordinate=pC-startingCorner
    vectorY:Coordinate=vectorAC-(vectorX*((vectorX.dot(vectorAC))/(vectorX.mag_sq())))

    xStep:Coordinate=vectorX/(cCount-1)
    yStep:Coordinate=vectorY/(rCount-1)

    totalCoordinates:list[Coordinate]=[]
    for y in range(rCount):
        for x in range(cCount):
            totalCoordinates.append((startingCorner+xStep*x+yStep*y).rounded())
    sessionData.clear_data_points()
    sessionData.add_data_points(totalCoordinates)
    
    """
    totalCoords: list[Coordinate]=[]
    for ind,pt in enumerate(pointCoords[:-1]):
        other: Coordinate=pointCoords[ind+1]
        totalCoords.append(pt)
        step: Coordinate=(other-pt)/(rCount-1)
        for ind in range(rCount-2):
            totalCoords.append((pt+(step*(ind+1))))
    totalCoords.append(pointCoords[-1])
    sessionData.clear_data_points()
    sessionData.add_data_points(totalCoords)
    """

def submit() -> None:
    recalculate()
    sessionData.submit_data_points()
    pointRecord.onsubmitpoints()


def generateIn(parentFrame:Frame) -> None:
    global rowCounter, colCounter
    rowCounter=StringVar()
    colCounter=StringVar()
    Button(parentFrame,text="Set point a",command=lambda: regPoint(0),font=TEXT_FONT).grid(row=0,column=0)
    Button(parentFrame,text="Set point b",command=lambda: regPoint(1),font=TEXT_FONT).grid(row=0,column=1)
    Button(parentFrame,text="Set point c",command=lambda: regPoint(2),font=TEXT_FONT).grid(row=0,column=2)
    Button(parentFrame,text="Submit", command=submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)

    Label(parentFrame,text="Enter row count").grid(row=2,column=0, padx=5)
    Entry(parentFrame,textvariable=rowCounter).grid(row=2,column=1, padx=5)
    rowCounter.trace_add("write", lambda a,b,c: rcounterUpdate(rowCounter))

    Label(parentFrame,text="Enter column count").grid(row=2,column=0, padx=5)
    Entry(parentFrame,textvariable=colCounter).grid(row=3,column=1, padx=5)
    colCounter.trace_add("write", lambda a,b,c: ccounterUpdate(colCounter))