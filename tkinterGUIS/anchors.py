from tkinter import Button,Frame,Label,StringVar
from helpers.configuration import *
from tkinterGUIS import connection, sessionData
from classes.coordinate import Coordinate
from classes.mover import mover
from classes.event import CustomEvent

_anchor_coords_vars:list[StringVar|None]=[None,None,None]
_anchor_coords:list[Coordinate|None]=[None, None, None]

onconfirmanchors:CustomEvent=CustomEvent()

def confirm() -> None:

    # send confirmation event when all coordinates are set
    if _anchor_coords[0] is not None and _anchor_coords[1] is not None and _anchor_coords[2] is not None:
        sessionData.set_local_anchors(_anchor_coords[0],_anchor_coords[1],_anchor_coords[2])
        onconfirmanchors()

def setAnchor(id:int) -> None:
    if connection.getStatus():
        _anchor_coords[id]=mover.get_coordinates()
        v:StringVar|None=_anchor_coords_vars[id]
        coords: Coordinate | None=_anchor_coords[id]
        if v is not None and coords is not None:
            v.set("X: "+str(coords.x)+"\nY: "+str(coords.y))
    pass


def generateIn(parentFrame:Frame) -> None:
    global _anchor_coords_vars

    _anchor_coords_vars[0]=StringVar()
    _anchor_coords_vars[1]=StringVar()
    _anchor_coords_vars[2]=StringVar()

    Label(parentFrame,font=TITLE_FONT, text="Anchors").grid(row=0,column=0,columnspan=3)
    
    Button(parentFrame, font=TEXT_FONT,command=lambda:setAnchor(0), text="Set anchor 1").grid(row=1,column=0)
    Button(parentFrame, font=TEXT_FONT,command=lambda:setAnchor(1), text="Set anchor 2").grid(row=1,column=1)
    Button(parentFrame, font=TEXT_FONT,command=lambda:setAnchor(2), text="Set anchor 3").grid(row=1,column=2)

    Label(parentFrame, font=TEXT_FONT, textvariable=_anchor_coords_vars[0]).grid(row=2,column=0)
    Label(parentFrame, font=TEXT_FONT, textvariable=_anchor_coords_vars[1]).grid(row=2,column=1)
    Label(parentFrame, font=TEXT_FONT, textvariable=_anchor_coords_vars[2]).grid(row=2,column=2)

    Button(parentFrame, font=TEXT_FONT, command=lambda:confirm(), text="Confirm").grid(row=3,column=0,columnspan=3)
    