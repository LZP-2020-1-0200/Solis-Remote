from tkinterGUIS  import connection
from classes  import sessionData
from helpers.configuration import TEXT_FONT
from classes.mover  import mover
from classes.coordinate import Coordinate
from classes.event import CustomEvent
from tkinter import StringVar, Frame,Button,Label,Entry, Misc

from classes.logger import Logger
import logging
log:logging.Logger=Logger(__name__).get_logger()

onsubmitpoints:CustomEvent=CustomEvent()
onsubmitpoints.bind(lambda:log.info("onsubmitpoints called"))

class GUI(Frame):
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        self._pointCounter: StringVar=StringVar()
        Button(self,text="Add point",command=self._regPoint,font=TEXT_FONT).grid(row=0,column=0)
        Button(self, text="Undo last point", command=self._unregPoint,font=TEXT_FONT).grid(row=0,column=1)
        Button(self,text="Submit", command=self._submit,font=TEXT_FONT).grid(row=1,column=0,columnspan=2)
        Label(self,text="Enter amount of points").grid(row=2,column=0, padx=5)
        Entry(self,textvariable=self._pointCounter).grid(row=2,column=1, padx=5)
        self._pointCounter.trace_add("write", lambda a,b,c: self._counterUpdate())
        self._ptCount:int=0
        self.pointCoords:list[Coordinate]=[]
        log.info("GUI init")

    def _counterUpdate(self) -> None:
        """Gets the number from the number of points entry and recalculates all points"""
        strVar:StringVar=self._pointCounter
        t: str=strVar.get()
        if t.isnumeric():
            self._ptCount=int(t)
        print(self._ptCount)
        self._recalculate()

    def _recalculate(self) -> None:
        """recalculates the intermediary points and refreshes pointDisplay"""
        totalCoords:list[Coordinate]=[]
        for ind,pt in enumerate(self.pointCoords[:-1]):
            other: Coordinate=self.pointCoords[ind+1]
            totalCoords.append(pt)
            step: Coordinate=(other-pt)/(self._ptCount-1)
            for ind in range(self._ptCount-2):
                totalCoords.append((pt+(step*(ind+1))).rounded())
        totalCoords.append(self.pointCoords[-1].rounded())
        sessionData.clear_data_points()
        sessionData.add_data_points(totalCoords)

    def _regPoint(self) -> None:
        """Adds the current stage position and recalculates points"""
        if connection.getStatus():
            coord:Coordinate
            coord=mover.get_coordinates()
            self.pointCoords.append(coord)
            self._recalculate()

    def _unregPoint(self) -> None:
        """Removes the last coordinate and recalculates points"""
        self.pointCoords.pop()
        self._recalculate()

    def _submit(self) -> None:
        self._recalculate()
        sessionData.submit_data_points()
        onsubmitpoints()