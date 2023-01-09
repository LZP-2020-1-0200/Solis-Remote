"""GUI for moving to n-th point"""
import logging
from tkinter import Frame, Entry, Button, Misc, StringVar, messagebox
from .PointRecording import point_display
from . import connection
from ..classes.session_data import data_struct
from ..classes.mover import mover
from ..classes.logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Generates a GUI for moving to Nth point"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self.point:StringVar=StringVar()
        self.last_index:int=0
        pd_gui:point_display.GUI=point_display.GUI(self)
        pd_gui.grid(column=0,row=0)
        pd_gui.display_points()
        side_bar:Frame=Frame(self)
        side_bar.grid(column=1,row=0)
        Entry(side_bar,textvariable=self.point).grid(column=0,row=0, columnspan=2)
        Button(side_bar,text="Go to point",command=self._go_to_point_var).grid(column=0, row=1, columnspan=1)
        Button(side_bar,text="Previous point", command=self._previous_point).grid(column=0, row=2)
        Button(side_bar,text="Next point", command=self._next_point).grid(column=1, row=2)

        log.info("GUI init")

    def _go_to_point(self) -> None:
        valid_num:bool=True
        if self.last_index>=len(data_struct.local_points) or self.last_index<0:
                valid_num=False
        if connection.get_status() and valid_num:
            if data_struct.local_points[self.last_index] is not None:
                mover.set_coordinates(data_struct.local_points[self.last_index].coordinate)
        else:
            messagebox.showwarning("Unable to go to point",#type: ignore
                "Entered index is invalid.")

    def _previous_point(self) -> None:
        self.last_index=max(0,self.last_index-1)
        self._go_to_point()
    
    def _next_point(self) -> None:
        self.last_index=min(len(data_struct.points)-1,self.last_index+1)
        self._go_to_point()

    def _go_to_point_var(self) -> None:
        valid_num:bool
        valid_num,self.last_index=self._strvar_to_int(self.point)
        log.info("Going to point %i", self.last_index)
        #transform to list index
        self.last_index-=1
        if valid_num:
            self._go_to_point()

    def _strvar_to_int(self,str_var:StringVar) -> tuple[bool,int]:
        """converts a `StringVar` variable's value to an `int`
        Returns a tuple of `bool` - was conversion successful, `int` - the value
        NOTE: the integer value is 0 if conversion was not successful
        """
        var_value: str=str_var.get()
        if var_value.isnumeric():
            return True, int(var_value)
        return False, 0
