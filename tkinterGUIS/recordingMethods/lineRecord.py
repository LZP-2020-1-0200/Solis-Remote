from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from classes.mover  import mover
from classes.coordinate import Coordinate
from tkinter import *


pointCoords:list[Coordinate]=[]

ptCount=0

def counterUpdate(strVar:StringVar):
    global ptCount
    t=strVar.get()
    if t.isnumeric():
        ptCount=int(t)
    print(ptCount)
    recalculate()

def recalculate():
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
    pointDisplay.displayPoints(ptl)


def regPoint():
    if connection.status:
        coord=mover.get_coordinates()
        pointCoords.append(coord)
        recalculate()
def unregPoint():
    pointCoords.pop()
    recalculate()