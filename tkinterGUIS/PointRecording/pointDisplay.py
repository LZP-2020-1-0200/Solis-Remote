from tkinter import Canvas, Label, Frame
from tkinterGUIS import sessionData
from classes.coordinate import Coordinate
from helpers.configuration import TEXT_FONT
from typing import Literal
import math

_canvas:Canvas|None=None
_sizeLabel:Label|None=None

CANVAS_PADDING: Literal[20]=20
CANVAS_SIZE: Literal[400]=400
POINT_SIZE: Literal[10]=10

def generateIn(parentFrame:Frame) -> None:
    """Generates the point display GUI inside `parentFrame`"""

    sessionData.onpointchange.bind(displayPoints)

    global _canvas, _sizeLabel
    _canvas=Canvas(parentFrame,width=CANVAS_SIZE,height=CANVAS_SIZE, bd = 2, bg = 'white', highlightthickness  = 1, highlightbackground = 'black')
    _canvas.grid(row=0,column=0, padx=5, pady=5)
    
    _sizeLabel=Label(parentFrame,font=TEXT_FONT,text="",justify="left", anchor="ne")
    _sizeLabel.grid(sticky='w',row=1,column=0)

def displayPoints() -> None:
    """Clears the canvas, draws all points from `sessionManager.pointList`, and updates the scale"""
    if _canvas is None:return

    points: list[Coordinate]=[item.coordinate for item in sessionData.dataStruct.local_points]

    _canvas.delete("all")
    
    # no need to draw anything if no points are present
    if len(points)==0:
        return

    # Acquires bounds of points
    min_x: int | float=points[0].x
    max_x: int | float=points[0].x
    min_y: int | float=points[0].y
    max_y: int | float=points[0].y
    for coord in points:
        x: int | float=coord.x
        y: int | float=coord.y
        min_x=min(x,min_x)
        max_x=max(x,max_x)
        min_y=min(y,min_y)
        max_y=max(y,max_y)
    
    # calculates the size of the field to get the scale
    size_x: int | float=max_x-min_x
    size_y: int | float=max_y-min_y
    max_size: int | float=max(size_x,size_y)
    if max_size>0:
        scale:float=(CANVAS_SIZE-2*CANVAS_PADDING)/max_size
        i:int=1
        for coord in points:
            x=CANVAS_SIZE/2  + ( (coord.x-(min_x+(size_x/2)))*scale )
            y=CANVAS_SIZE/2  + ( (coord.y-(min_y+(size_y/2)))*scale )
            _canvas.create_oval(x-POINT_SIZE/2,y-POINT_SIZE/2,x+POINT_SIZE/2,y+POINT_SIZE/2,fill="red", outline="")
            _canvas.create_text(x-POINT_SIZE,y-POINT_SIZE,text=str(i)+".")
            i+=1
        rounded10:float=10**math.floor(math.log10(max_size))
        _canvas.create_line(rounded10*scale+3,CANVAS_SIZE-2,rounded10*scale+3,CANVAS_SIZE-CANVAS_PADDING+2,fill="black")
        _canvas.create_line(3,CANVAS_SIZE-2,3,CANVAS_SIZE-CANVAS_PADDING+2,fill="black")
        _canvas.create_line(3,CANVAS_SIZE-CANVAS_PADDING/2,rounded10*scale+3,CANVAS_SIZE-CANVAS_PADDING/2,fill="black")
        if _sizeLabel is not None:
            _sizeLabel.config(text=str(rounded10)+"μm")

    #because the scale doesn't make sense when the size is 0, the points are all drawn in the center when that is the case
    else:
        for coord in points:
            _canvas.create_oval(CANVAS_SIZE/2-POINT_SIZE/2,CANVAS_SIZE/2-POINT_SIZE/2,CANVAS_SIZE/2+POINT_SIZE/2,CANVAS_SIZE/2+POINT_SIZE/2,fill="red", outline="")

    
sessionData.onpointchange.bind(displayPoints)
    
    