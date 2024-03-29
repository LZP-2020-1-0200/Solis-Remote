"""Contains a GUI class that creates a Canvas for displaying points and scale"""
from typing import Literal
import math
import logging
from tkinter import Canvas, Label, Frame, Misc
from ...classes import session_data
from ...classes.coordinate import Coordinate
from ...helpers.configuration import TEXT_FONT

from ...classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()


CANVAS_PADDING: Literal[20]=20
CANVAS_SIZE: Literal[400]=400
POINT_SIZE: Literal[10]=10


class GUI(Frame):
    """Generates a GUI that displays registered points"""
    def __init__(self,parent:Misc) -> None:
        Frame.__init__(self,parent)
        session_data.data_struct.onpointchange.bind(self.display_points)
        self._canvas: Canvas=Canvas(self,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            bd = 2,
            bg = 'white',
            highlightthickness  = 1,
            highlightbackground = 'black')
        self._canvas.grid(row=0,column=0, padx=5, pady=5)
        self._size_label: Label=Label(self,font=TEXT_FONT,text="",justify="left", anchor="ne")
        self._size_label.grid(sticky='w',row=1,column=0)
        log.info("GUI init")

    def display_points(self) -> None:
        """Clears the canvas,
        draws all points from `sessionManager.pointList`,
        and updates the scale
        """
        log.info("Displaying points")
        points: list[Coordinate]=[item.coordinate for item in session_data.data_struct.local_points]

        self._canvas.delete("all")

        # no need to draw anything if no points are present
        if len(points)==0:
            return

        # Acquires bounds of points
        min_x: int | float=points[0].x
        max_x: int | float=points[0].x
        min_y: int | float=points[0].y
        max_y: int | float=points[0].y
        for coord in points:
            min_x=min(coord.x,min_x)
            max_x=max(coord.x,max_x)
            min_y=min(coord.y,min_y)
            max_y=max(coord.y,max_y)

        # calculates the size of the field to get the scale
        size_x: int | float=max_x-min_x
        size_y: int | float=max_y-min_y
        max_size: int | float=max(size_x,size_y)
        if max_size>0:
            scale:float=(CANVAS_SIZE-2*CANVAS_PADDING)/max_size
            i:int=1
            for coord in points:
                x_coord: float=CANVAS_SIZE/2  - ( (coord.x-(min_x+(size_x/2)))*scale )
                y_coord: float=CANVAS_SIZE/2  - ( (coord.y-(min_y+(size_y/2)))*scale )
                self._canvas.create_oval(
                    x_coord-POINT_SIZE/2,
                    y_coord-POINT_SIZE/2,
                    x_coord+POINT_SIZE/2,
                    y_coord+POINT_SIZE/2,
                    fill="red", outline="")
                self._canvas.create_text(x_coord-POINT_SIZE,y_coord-POINT_SIZE,text=str(i)+".")
                i+=1
            rounded10:float=10**math.floor(math.log10(max_size))
            self._canvas.create_line(
                rounded10*scale+3,  CANVAS_SIZE-2,
                rounded10*scale+3,  CANVAS_SIZE-CANVAS_PADDING+2,
                fill="black")
            self._canvas.create_line(
                3,CANVAS_SIZE-2,
                3,CANVAS_SIZE-CANVAS_PADDING+2,
                fill="black")
            self._canvas.create_line(
                3,CANVAS_SIZE-CANVAS_PADDING/2,
                rounded10*scale+3,CANVAS_SIZE-CANVAS_PADDING/2,
                fill="black")
            self._size_label.config(text=str(rounded10)+"μm")

        # because the scale doesn't make sense when the size is 0,
        # the points are all drawn in the center when that is the case
        else:
            for coord in points:
                self._canvas.create_oval(
                    CANVAS_SIZE/2-POINT_SIZE/2,CANVAS_SIZE/2-POINT_SIZE/2,
                    CANVAS_SIZE/2+POINT_SIZE/2,CANVAS_SIZE/2+POINT_SIZE/2,
                    fill="red", outline="")
