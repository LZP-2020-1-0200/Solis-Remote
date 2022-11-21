from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from classes.mover  import mover
from classes.coordinate import Coordinate
from tkinter import *


pointCoords:list[Coordinate]=[]

pointCounter:StringVar=None

ptCount=0

def counterUpdate(strVar:StringVar):
    """Gets the number from the number of points entry and recalculates all points"""
    global ptCount
    t=strVar.get()
    if t.isnumeric():
        ptCount=int(t)
    print(ptCount)
    recalculate()

def recalculate():
    """recalculates the intermediary points and refreshes pointDisplay"""
    totalCoords=[]
    for ind,pt in enumerate(pointCoords[:-1]):
        other=pointCoords[ind+1]
        totalCoords.append(pt)
        step=(other-pt)/(ptCount+1)
        for i in range(1,ptCount+1):
            totalCoords.append(pt+(step*i))
    totalCoords.append(pointCoords[-1])
    ptl=[(c.x,c.y) for c in totalCoords]
    sessionManager.pointList=ptl
    pointDisplay.displayPoints()


def regPoint():
    """Adds the current stage position and recalculates points"""
    if connection.getStatus():
        coord=mover.get_coordinates()
        pointCoords.append(coord)
        recalculate()
def unregPoint():
    """Removes the last coordinate and recalculates points"""
    pointCoords.pop()
    recalculate()


