from tkinter import * 
from collections.abc import Callable
from tkinterGUIS import sessionManager
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
import math

_canvas:Canvas=None
_sizeLabel:Label=None

CANVAS_PADDING=20
CANVAS_SIZE=400
POINT_SIZE=10

def generateIn(parentFrame):
    """Generates the point display GUI inside `parentFrame`"""

    global _canvas, _sizeLabel
    _canvas=Canvas(parentFrame,width=CANVAS_SIZE,height=CANVAS_SIZE, bd = 2, bg = 'white', highlightthickness  = 1, highlightbackground = 'black')
    _canvas.grid(row=0,column=0, padx=5, pady=5)
    
    _sizeLabel=Label(parentFrame,font=TEXT_FONT,text="",justify="left", anchor="ne")
    _sizeLabel.grid(sticky=W,row=1,column=0)
    

def displayPoints():
    """Clears the canvas, draws all points from `sessionManager.pointList`, and updates the scale"""

    points=sessionManager.pointList

    _canvas.delete("all")
    
    # no need to draw anything if no points are present
    if len(points)==0:
        return

    # Acquires bounds of points
    min_x=points[0][0]
    max_x=points[0][0]
    min_y=points[0][1]
    max_y=points[0][1]
    for coord in points:
        x=coord[0]
        y=coord[1]
        min_x=min(x,min_x)
        max_x=max(x,max_x)
        min_y=min(y,min_y)
        max_y=max(y,max_y)
    
    # calculates the size of the field to get the scale
    size_x=max_x-min_x
    size_y=max_y-min_y
    max_size=max(size_x,size_y)
    if max_size>0:
        scale=(CANVAS_SIZE-2*CANVAS_PADDING)/max_size
        i=1
        for coord in points:
            x=CANVAS_SIZE/2  + ( (coord[0]-(min_x+(size_x/2)))*scale )
            y=CANVAS_SIZE/2  + ( (coord[1]-(min_y+(size_y/2)))*scale )
            _canvas.create_oval(x-POINT_SIZE/2,y-POINT_SIZE/2,x+POINT_SIZE/2,y+POINT_SIZE/2,fill="red", outline="")
            _canvas.create_text(x-POINT_SIZE,y-POINT_SIZE,text=str(i)+".")
            i+=1
        rounded10=10**math.floor(math.log10(max_size))
        _canvas.create_line(rounded10*scale+3,CANVAS_SIZE-2,rounded10*scale+3,CANVAS_SIZE-CANVAS_PADDING+2,fill="black")
        _canvas.create_line(3,CANVAS_SIZE-2,3,CANVAS_SIZE-CANVAS_PADDING+2,fill="black")
        _canvas.create_line(3,CANVAS_SIZE-CANVAS_PADDING/2,rounded10*scale+3,CANVAS_SIZE-CANVAS_PADDING/2,fill="black")
        _sizeLabel.config(text=str(rounded10)+"μm")

    #because the scale doesn't make sense when the size is 0, the points are all drawn in the center when that is the case
    else:
        for coord in points:
            _canvas.create_oval(CANVAS_SIZE/2-POINT_SIZE/2,CANVAS_SIZE/2-POINT_SIZE/2,CANVAS_SIZE/2+POINT_SIZE/2,CANVAS_SIZE/2+POINT_SIZE/2,fill="red", outline="")

    
    
    
    