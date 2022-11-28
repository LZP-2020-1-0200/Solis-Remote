
from tkinterGUIS  import connection
from tkinterGUIS import sessionData
from classes.mover  import mover
from classes.coordinate import Coordinate
from tkinter import StringVar


markers:list[Coordinate]=[Coordinate(0,0),Coordinate(1,0),Coordinate(0,1)]
markerText:StringVar=None
a:Coordinate=None
b:Coordinate=None

def updateText():
    global markers, markerText
    markerText.set("".join([("{"+str(marker)+"},") for ind, marker in enumerate(markers)]))

def regMarker(n:int)->None:
    global markers, markerText
    if connection.getStatus():
        coord=mover.get_coordinates()
        markers[n]=coord
    updateText()

def generateMarkerVectors()->None:
    a=markers[1]-markers[0]
    b=markers[2]-markers[0]

def toMarkerCoords(c:Coordinate)->Coordinate:
    return Coordinate(c.asComponentOf(a),c.asComponentOf(b))

def saveMarkers():
    sessionData.set_local_anchors(markers[0],markers[1],markers[2])