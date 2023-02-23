"""Contains a GUI class for recording points in a rectangle pattern"""
from tkinter import Button, Label, StringVar, Frame, Entry, messagebox
import logging
from ....helpers.configuration import TEXT_FONT
from ....classes  import session_data, MicroscopeMover, Coordinate, CustomEvent, Logger, MicroscopeStatus

log:logging.Logger=Logger(__name__).get_logger()



class GUI(Frame):
    """Generates the GUI for rectangle point registration"""
    def __init__(self,parent:Frame) -> None:
        Frame.__init__(self, parent)
        self._row_counter: StringVar=StringVar()
        self._col_counter: StringVar=StringVar()
        self._r_count:int=2
        self._c_count:int=2
        self.onsubmitpoints:CustomEvent=CustomEvent("rectangle_recordingGUI.onsubmitpoints")
        Button(self,
            text="Set point A",
            command=lambda:self._reg_point(0),
            font=TEXT_FONT
            ).grid(row=0,column=0)
        Button(self,
            text="Set point B",
            command=lambda:self._reg_point(1),
            font=TEXT_FONT
            ).grid(row=0,column=1)
        Button(self,
            text="Set point C",
            command=lambda:self._reg_point(2),
            font=TEXT_FONT
            ).grid(row=0,column=2)
        Button(self,
            text="Submit",
            command=self._submit,
            font=TEXT_FONT
            ).grid(row=1,column=0,columnspan=2)

        Label(self,text="Enter row count").grid(row=2,column=0, padx=5)
        Entry(self,textvariable=self._row_counter).grid(row=2,column=1, padx=5)
        self._row_counter.trace_add("write", lambda a,b,c: self._rcounter_update())

        Label(self,text="Enter column count").grid(row=3,column=0, padx=5)
        Entry(self,textvariable=self._col_counter).grid(row=3,column=1, padx=5)
        self._col_counter.trace_add("write", lambda a,b,c: self._ccounter_update())
        self._points:list[Coordinate|None]=[None,None,None]
        log.info("GUI init")

    def _reg_point(self, ind:int) -> None:
        """Gets the coordinates and registers them as the point with index `id`"""
        with MicroscopeMover() as mover:
            if mover.last_status==MicroscopeStatus.CONNECTED:
                self._points[ind]=mover.get_coordinates()
                self._recalculate()
                messagebox.showinfo("Info", "Point registered")#type: ignore

    def _strvar_to_int(self,str_var:StringVar) -> tuple[bool,int]:
        """converts a `StringVar` variable's value to an `int`
        Returns a tuple of `bool` - was conversion successful, `int` - the value
        NOTE: the integer value is 0 if conversion was not successful
        """
        var_value: str=str_var.get()
        if var_value.isnumeric():
            return True, int(var_value)
        return False, 0

    def _rcounter_update(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        self._r_count=max(2,self._strvar_to_int(self._row_counter)[1])
        log.info("Rows set to %i", self._r_count)
        self._recalculate()

    def _ccounter_update(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        self._c_count=max(2,self._strvar_to_int(self._col_counter)[1])
        log.info("Rows set to %i", self._c_count)
        self._recalculate()

    def _recalculate(self) -> None:
        """recalculates the intermediary points and refreshes pointDisplay"""
        assert self._r_count>=2 and self._c_count>=2
        point_a:Coordinate|None=self._points[0]
        point_b:Coordinate|None=self._points[1]
        point_c:Coordinate|None=self._points[2]
        if point_a is None or point_b is None or point_c is None:
            log.info("Not all points were selected. A set: %s, B set: %s, C set: %s",
                point_a is not None,
                point_b is not None,
                point_c is not None)
            return
        rect_x:Coordinate=point_b-point_a
        vector_ac:Coordinate=point_c-point_a
        distance_to_height: Coordinate=(rect_x*((rect_x.dot(vector_ac))/(rect_x.mag_sq())))
        rect_y:Coordinate=vector_ac-distance_to_height

        #there are 1 fewer segments than points
        x_step:Coordinate=rect_x/(self._c_count-1)
        y_step:Coordinate=rect_y/(self._r_count-1)

        total_coordinates:list[Coordinate]=[]
        for y_index in range(self._r_count):
            for x_index in range(self._c_count):
                total_coordinates.append((point_a+(x_step*x_index)+(y_step*y_index)).rounded())
        #replace all datapoints
        session_data.clear_data_points()
        session_data.add_data_points(total_coordinates)

    def _submit(self) -> None:
        self._recalculate()
        session_data.submit_data_points()
        self.onsubmitpoints()
