from tkinter import Frame, Button, Label, StringVar, Toplevel, messagebox, Radiobutton
from classes.mover import mover
from tkinterGUIS import connection
from tkinterGUIS import sessionData
from helpers import configuration
from tkinterGUIS import sessionData
from helpers.configuration import TEXT_FONT
import math
import os
from typing import Literal



def takeReference(referenceType:int) -> None:
    if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
        return
    if connection.getStatus():
        i:int=1
        fullDir:str=""
        relDir:str=""
        filename:str=""
        while True:
            filename=configuration.referenceNames[referenceType]+str(i).zfill(2)+".asc"
            relDir=os.path.join("refs",filename)
            fullDir=os.path.join(sessionData.dataStruct.dir,relDir)
            if not os.path.isfile(fullDir):
                break
            i+=1
        
        sessionData.add_reference(relDir,configuration.referenceNames[referenceType])
        mover.set_output_directory(os.path.join(sessionData.dataStruct.dir,"refs"))
        mover.take_capture(filename)


def run() -> None:
    if not messagebox.askyesno("","Is SOLIS script on?"):#type: ignore
        return
    if connection.getStatus():
        #finds the lowest unused experiment number
        i:int=0
        experimentDir: str=""
        while True:
            experimentDir=os.path.join(sessionData.dataStruct.dir,"experiments", str(i).zfill(3) )
            if not os.path.isdir(experimentDir):
                os.mkdir(experimentDir)
                break
            i+=1

        if experimentDir is not None:

            #Generates an environment popup
            tp: Toplevel=Toplevel()
            tp.title("Select an environment")
            experimentMedium: StringVar=StringVar()
            #lists all environments in a square
            s: int=math.ceil(math.sqrt(len(configuration.media)))
            for ind, med in enumerate(configuration.media):
                Radiobutton(tp, text = med, variable = experimentMedium, indicatoron=False,
                        value = med,
                        background = "light blue").grid(row=ind//s,column=ind%s,ipady = 5,ipadx=5,sticky="news")
            tp.wait_variable(experimentMedium)
            #Confirmation button appears only after an environment has been selected
            var: StringVar = StringVar()
            button: Button = Button(tp, text="Set", command=lambda: var.set("1"))
            button.grid(row=s,column=0,columnspan=s,sticky="news",ipady=5, ipadx = 5)
            button.wait_variable(var)
            
            #add the experiment to sessionData and close the popup
            sessionData.add_experiment(os.path.relpath(experimentDir,sessionData.dataStruct.dir),experimentMedium.get())
            tp.destroy()

            #launch the experiment
            mover.set_output_directory(experimentDir)
            for pt in sessionData.dataStruct.local_points:
                mover.set_coordinates(pt.coordinate)
                mover.take_capture(pt.filename)

_CHECK: Literal['✓']="✓"
_CROSS: Literal['✗']="✗"

point_status:StringVar|None=None
marker_status:StringVar|None=None
local_marker_status:StringVar|None=None

def statusUpdate() -> None:
    assert point_status         is not None
    assert marker_status        is not None 
    assert local_marker_status  is not None
    assert startB               is not None
    #{"points_set":False,"anchors_set":False}
    if sessionData.dataStruct.points_set:
        point_status.set(_CHECK)
    else:
        point_status.set(_CROSS)
    if sessionData.dataStruct.anchors_set:
        marker_status.set(_CHECK)
    else:
        marker_status.set(_CROSS)
    if sessionData.dataStruct.local_anchors_set:
        local_marker_status.set(_CHECK)
    else:
        local_marker_status.set(_CROSS)
    if sessionData.dataStruct.points_set and sessionData.dataStruct.anchors_set and sessionData.dataStruct.local_anchors_set:
        startB["state"]="normal"
    else:
        startB["state"]="disabled"
sessionData.onstatuschange.bind(statusUpdate)

startB:Button|None=None

def generateIn(parentFrame:Frame) -> None:
    global point_status, marker_status, local_marker_status, startB
    point_status=StringVar()
    marker_status=StringVar()
    local_marker_status=StringVar()
    

    startB = Button(parentFrame, text="Launch experiment", font=TEXT_FONT, command=run)
    startB.grid(row=0,column=1, padx=5,sticky="news")

    checklist: Frame=Frame(parentFrame)
    checklist.grid(row=0,column=0)

    checkLabel1: Label=Label(checklist, text="Points", font=TEXT_FONT)
    checkLabel1.grid(row=0,column=0)

    checkLabel2: Label=Label(checklist, text="Anchors", font=TEXT_FONT)
    checkLabel2.grid(row=1,column=0)

    checkLabel3: Label=Label(checklist, text="Local anchors", font=TEXT_FONT)
    checkLabel3.grid(row=2,column=0)

    checkStatus1: Label=Label(checklist,textvariable=point_status, font=TEXT_FONT)
    checkStatus1.grid(row=0,column=1)

    checkStatus2: Label=Label(checklist,textvariable=marker_status, font=TEXT_FONT)
    checkStatus2.grid(row=1,column=1)

    checkStatus3: Label=Label(checklist,textvariable=local_marker_status, font=TEXT_FONT)
    checkStatus3.grid(row=2,column=1)

    
    statusUpdate()

    

    

