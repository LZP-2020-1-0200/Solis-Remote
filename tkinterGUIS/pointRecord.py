from tkinter import * 
from collections.abc import Callable
from tkinterGUIS  import connection
from tkinterGUIS  import sessionManager
from tkinterGUIS  import pointDisplay
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
from classes.mover  import mover
from tkinterGUIS.recordingMethods import manualRecord
from tkinterGUIS.recordingMethods import lineRecord
from tkinterGUIS.recordingMethods import markers

parent:Frame=None
regMethod:IntVar=None
methodWidgets:list[list[Widget]]=[]
radios:list[Radiobutton]=[]

def submitMarkers():
    """Removes the ability to change marker positions"""

    regMethod.set(1)
    methodChange()
    for r in radios:
        r.grid()


def methodChange():
    """Switches the GUIS to the appropriate point registration method"""
    for ws in methodWidgets:
        for widget in ws:
            widget.grid_remove()
    for widget in methodWidgets[regMethod.get()]:
        widget.grid()
    pass

def generateIn(parentFrame):
    """Generates the point recording GUI inside `parentFrame`"""

    global parent, methodWidgets, regMethod, radios
    regMethod=IntVar()
    lineRecord.pointCounter=StringVar()
    markers.markerText=StringVar()
    markers.updateText()

    parent=parentFrame
    title=Label(parentFrame,text="Point registration",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    markerFrame=Frame(parentFrame)
    markerFrame.grid(row=1,column=0,columnspan=2)
    markerButton=Button(markerFrame, font=TEXT_FONT,text="Set marker 1",command=lambda:markers.regMarker(0))
    markerButton.grid(row=0,column=0)
    markerButton2=Button(markerFrame, font=TEXT_FONT,text="Set marker 2",command=lambda:markers.regMarker(1))
    markerButton2.grid(row=0,column=1)
    markerButton3=Button(markerFrame, font=TEXT_FONT,text="Set marker 3",command=lambda:markers.regMarker(2))
    markerButton3.grid(row=0,column=2)
    markerLabel=Label(markerFrame, font=TEXT_FONT,textvariable=markers.markerText)
    markerLabel.grid(row=1,column=0,columnspan=3)
    markerSubmit=Button(markerFrame, font=TEXT_FONT,text="Submit",command=submitMarkers)
    markerSubmit.grid(row=2,column=0,columnspan=3)

    #Manual points
    radioManualPoints=Radiobutton(parentFrame,text="Manual registration",value=1,variable=regMethod,command=methodChange)
    radioManualPoints.grid(row=2,column=0,sticky="news")
    radioManualPoints.grid_remove()
    radios.append(radioManualPoints)


    registerButton = Button(parentFrame,text="Register point", font=TEXT_FONT, command=manualRecord.regPoint)
    registerButton.grid(row=3,column=0, padx=5)

    undoButton = Button(parentFrame,text="Undo last point", font=TEXT_FONT, command=manualRecord.unregPoint)
    undoButton.grid(row=3,column=1,padx=5)


    #Lines
    radioLine=Radiobutton(parentFrame,text="Line Registration",value=2,variable=regMethod,command=methodChange)
    radioLine.grid(row=2,column=1,sticky="news")
    radioLine.grid_remove()
    radios.append(radioLine)

    lineRegisterButton = Button(parentFrame,text="Register point", font=TEXT_FONT, command=lineRecord.regPoint)
    lineRegisterButton.grid(row=3,column=0, padx=5)

    lineUndoButton = Button(parentFrame,text="Undo last point", font=TEXT_FONT, command=lineRecord.unregPoint)
    lineUndoButton.grid(row=3,column=1,padx=5)
    
    linePtCountLabel=Label(parentFrame,text="Enter amount of points")
    linePtCountLabel.grid(row=4,column=0, padx=5)

    linePtCount=Entry(parentFrame,textvariable=lineRecord.pointCounter)
    linePtCount.grid(row=4,column=1, padx=5)
    lineRecord.pointCounter.trace_add("write", lambda a,b,c: lineRecord.counterUpdate(lineRecord.pointCounter))

    #Square
    radioLine=Radiobutton(parentFrame,text="Square Registration",value=3,variable=regMethod,command=methodChange)
    radioLine.grid(row=2,column=2,sticky="news")
    radioLine.grid_remove()
    radios.append(radioLine)

    squareRegister1Button = Button(parentFrame,text="Register first point", font=TEXT_FONT, command=lineRecord.regPoint)
    squareRegister1Button.grid(row=3,column=0, padx=5)

    squareRegister2Button = Button(parentFrame,text="Register second point", font=TEXT_FONT, command=lineRecord.unregPoint)
    squareRegister2Button.grid(row=3,column=1,padx=5)
    
    squarePtCountLabel=Label(parentFrame,text="Enter amount of points")
    squarePtCountLabel.grid(row=4,column=0, padx=5)

    squarePtCount=Entry(parentFrame,textvariable=lineRecord.pointCounter)
    squarePtCount.grid(row=4,column=1, padx=5)

    squareRowCountLabel=Label(parentFrame,text="Enter amount of points")
    squareRowCountLabel.grid(row=4,column=0, padx=5)

    squareRowCount=Entry(parentFrame,textvariable=lineRecord.pointCounter)
    squareRowCount.grid(row=4,column=1, padx=5)
    #pointCounter.trace_add("write", lambda a,b,c: lineRecord.counterUpdate(pointCounter))

    methodWidgets=[
        [markerFrame],
        [registerButton,undoButton],
        [lineRegisterButton,lineUndoButton,linePtCountLabel,linePtCount],
        [squareRegister1Button,squareRegister2Button,squarePtCountLabel,squarePtCount,squareRowCountLabel,squareRowCount]
    
    ]
    regMethod.set(0)
    methodChange()
    #radioManualPoints.select()





