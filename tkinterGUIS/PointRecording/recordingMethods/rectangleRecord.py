from tkinterGUIS  import connection
from classes  import sessionData
from helpers.configuration import TEXT_FONT
from classes.mover  import mover
from classes.coordinate import Coordinate
from classes.event import CustomEvent
from tkinter import Button, Label, StringVar, Frame, Entry

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))

#pointCoords:list[Coordinate]=[]

#rowCounter:StringVar|None=None
#colCounter:StringVar|None=None

#rCount:int=2
#cCount:int=2

#points:list[Coordinate|None]=[None,None,None]

class GUI(Frame):
    def __init__(self,parent:Frame) -> None:
        Frame.__init__(self, parent)
        self._rowCounter: StringVar=StringVar()
        self._colCounter: StringVar=StringVar()
        self._rCount:int=2
        self._cCount:int=2
        Button(self,text="Set point a",command=lambda: self._regPoint(0),font=TEXT_FONT).grid(row=0,column=0)
        Button(self,text="Set point b",command=lambda: self._regPoint(1),font=TEXT_FONT).grid(row=0,column=1)
        Button(self,text="Set point c",command=lambda: self._regPoint(2),font=TEXT_FONT).grid(row=0,column=2)
        Button(self,text="Submit", command=self._submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)

        Label(self,text="Enter row count").grid(row=2,column=0, padx=5)
        Entry(self,textvariable=self._rowCounter).grid(row=2,column=1, padx=5)
        self._rowCounter.trace_add("write", lambda a,b,c: self._rcounterUpdate())

        Label(self,text="Enter column count").grid(row=2,column=0, padx=5)
        Entry(self,textvariable=self._colCounter).grid(row=3,column=1, padx=5)
        self._colCounter.trace_add("write", lambda a,b,c: self._ccounterUpdate())
        self._points:list[Coordinate|None]=[None,None,None]
        log.info("GUI init")
    def _regPoint(self,ind:int) -> None:
        if connection.getStatus():
            self._points[ind]=mover.get_coordinates()
            self._recalculate()

    def _rcounterUpdate(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        t: str=self._rowCounter.get()
        if t.isnumeric():
            self._rCount=int(t)
        self._rCount=max(2,self._rCount)
        print(self._rCount)
        self._recalculate()

    def _ccounterUpdate(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        t: str=self._colCounter.get()
        if t.isnumeric():
            self._cCount=int(t)
        self._cCount=max(2,self._cCount)
        print(self._cCount)
        self._recalculate()

    def _recalculate(self) -> None:
        """recalculates the intermediary points and refreshes pointDisplay"""
        assert self._rCount>=2 and self._cCount>=2
        startingCorner:Coordinate|None=self._points[0]
        pB:Coordinate|None=self._points[1]
        pC:Coordinate|None=self._points[2]
        if startingCorner is None or pB is None or pC is None: return
        vectorX:Coordinate=pB-startingCorner
        vectorAC:Coordinate=pC-startingCorner
        vectorY:Coordinate=vectorAC-(vectorX*((vectorX.dot(vectorAC))/(vectorX.mag_sq())))

        xStep:Coordinate=vectorX/(self._cCount-1)
        yStep:Coordinate=vectorY/(self._rCount-1)

        totalCoordinates:list[Coordinate]=[]
        for y in range(self._rCount):
            for x in range(self._cCount):
                totalCoordinates.append((startingCorner+xStep*x+yStep*y).rounded())
        sessionData.clear_data_points()
        sessionData.add_data_points(totalCoordinates)

    def _submit(self) -> None:
        self._recalculate()
        sessionData.submit_data_points()
        onsubmitpoints()


    