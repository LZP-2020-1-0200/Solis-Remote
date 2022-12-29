"""Contains the class for generating line registration GUI"""
import logging
from tkinter import StringVar, Frame,Button,Label,Entry, Misc

from ....guis  import connection
from ....classes  import session_data
from ....helpers.configuration import TEXT_FONT
from ....classes.mover  import mover
from ....classes.coordinate import Coordinate
from ....classes.event import CustomEvent

from ....classes.logger import Logger
log:logging.Logger=Logger(__name__).get_logger()

onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))

class GUI(Frame):
    """Generates a GUI for recording lines"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._point_counter: StringVar=StringVar()
        Button(self,
            text="Add point",
            command=self._reg_point,
            font=TEXT_FONT
            ).grid(row=0,column=0)
        Button(self,
            text="Undo last point",
            command=self._unreg_point,
            font=TEXT_FONT
            ).grid(row=0,column=1)
        Button(self,
            text="Submit",
            command=self._submit,
            font=TEXT_FONT
            ).grid(row=1,column=0,columnspan=2)
        Label(self,text="Enter amount of points").grid(row=2,column=0, padx=5)
        Entry(self,textvariable=self._point_counter).grid(row=2,column=1, padx=5)
        self._point_counter.trace_add("write", lambda a,b,c: self._counter_update())
        self._pt_count:int=0
        self.point_coords:list[Coordinate]=[]
        log.info("GUI init")

    def _strvar_to_int(self,str_var:StringVar) -> tuple[bool,int]:
        """converts a `StringVar` variable's value to an `int`
        Returns a tuple of `bool` - was conversion successful, `int` - the value
        NOTE: the integer value is 0 if conversion was not successful
        """
        var_value: str=str_var.get()
        if var_value.isnumeric():
            return True, int(var_value)
        return False, 0

    def _counter_update(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        self._pt_count=max(2,self._strvar_to_int(self._point_counter)[1])
        log.info("Rows set to %i", self._pt_count)
        self._recalculate()

    def _recalculate(self) -> None:
        """recalculates the intermediary points and refreshes pointDisplay"""
        total_coords:list[Coordinate]=[]
        for ind, point in enumerate(self.point_coords[:-1]):
            other: Coordinate=self.point_coords[ind+1]
            total_coords.append(point)
            step: Coordinate=(other-point)/(self._pt_count-1)
            for ind in range(self._pt_count-2):
                total_coords.append((point+(step*(ind+1))).rounded())
        total_coords.append(self.point_coords[-1].rounded())
        session_data.clear_data_points()
        session_data.add_data_points(total_coords)

    def _reg_point(self) -> None:
        """Adds the current stage position and recalculates points"""
        if connection.get_status():
            coord:Coordinate
            coord=mover.get_coordinates()
            self.point_coords.append(coord)
            self._recalculate()

    def _unreg_point(self) -> None:
        """Removes the last coordinate and recalculates points"""
        self.point_coords.pop()
        self._recalculate()

    def _submit(self) -> None:
        self._recalculate()
        session_data.submit_data_points()
        onsubmitpoints()
