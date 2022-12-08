from tkinter import Frame
from tkinterGUIS.mainMenu import pointPointer, sessionManager, referenceManager


_ref_frame:Frame|None=None
_point_frame:Frame|None=None
_bottom_frame:Frame|None=None


def generateIn(parent:Frame) -> None:
    global _ref_frame, _point_frame, _bottom_frame
    _point_frame=Frame(parent)
    pointPointer.generateIn(_point_frame)
    _point_frame.grid(row=0,column=1)

    _ref_frame=Frame(parent)
    referenceManager.generateIn(_ref_frame)
    _ref_frame.grid(row=0,column=0)

    

    _bottom_frame=Frame(parent)
    _bottom_frame.grid(row=1,column=0,columnspan=2)
    sessionManager.generateIn(_bottom_frame)


    
