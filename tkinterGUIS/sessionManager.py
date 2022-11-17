from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from classes.mover import mover
from classes.coordinate import Coordinate
from tkinterGUIS import connection
from tkinterGUIS import sessionSetup
from tkinterGUIS import pointDisplay
from tkinterGUIS import pointRecord
from tkinterGUIS import configuration
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT
import classes.coordinate
from collections.abc import Callable
from os.path import relpath
import json
import datetime
import math
import os

sessionData={}
dir=None

def updateSessionData():
    global dir
    with open(dir+"/session.json", "w") as outfile:
        outfile.write(json.dumps(sessionData, indent=4))
        outfile.close()

preExperimentWidgets:Widget=[]
experimentWidgets:Widget=[]

def selectSession():
    global dir, sessionData, pointList
    dir=filedialog.askdirectory(title='Select session directory').replace("/","\\")
    f = open(dir+'/session.json')
    sessionData=json.load(f)
    f.close()
    jsonPoints=sessionData["points"]
    pointList=[]
    for pt in jsonPoints:
        pointList.append((pt["x"],pt["y"]))
    pointDisplay.displayPoints(pointList)
    for w in preExperimentWidgets:
        w.grid_remove()
    for w in experimentWidgets:
        w.grid()
    statusStr.set(f"Session: {dir}")
    
    

def createSession():
    global dir, sessionData
    
    dir=filedialog.askdirectory(title="Select directory of new session").replace("/","\\")
    
    sessionData=sessionSetup.sessionSetup(dir,pointList)
    for w in preExperimentWidgets:
        w.grid_remove()
    for w in experimentWidgets:
        w.grid()
    statusStr.set(f"Session: {dir}")
    



def takeReference(referenceType:int):
    global dir
    if not messagebox.askyesno("","Is SOLIS script on?"):
        return
    if connection.getStatus():
        i=1
        fullDir=None
        relDir=None
        filename=None
        while True:
            filename=configuration.referenceNames[referenceType]+str(i).zfill(2)+".asc"
            relDir=os.path.join("refs",filename)
            fullDir=os.path.join(dir,relDir)
            if not os.path.isfile(fullDir):
                break
            i+=1
        sessionData["refs"].append({"file":relDir,"type":configuration.referenceNames[referenceType],"timestamp":str(datetime.datetime.now())})
        updateSessionData()
        mover.send_custom_command("SDIR "+os.path.join(dir,"refs"))
        mover.send_custom_command(f"RUN {filename}")


def run():
    global dir
    if not messagebox.askyesno("","Is SOLIS script on?"):
        return
    if connection.getStatus():
        i=0
        experimentDir=None
        while True:
            experimentDir=os.path.join(dir,"experiments", str(i).zfill(3) )

            if not os.path.isdir(experimentDir):
                os.mkdir(experimentDir)
                break
            i+=1

        if not (experimentDir==None):
            tp=Toplevel()
            tp.title("Select an environment")
            experimentMedium=StringVar()
            s=math.ceil(math.sqrt(len(configuration.mediums)))
            for ind, med in enumerate(configuration.mediums):
                Radiobutton(tp, text = med, variable = experimentMedium,
                        value = med, indicator = 0,
                        background = "light blue").grid(row=ind//s,column=ind%s,ipady = 5,ipadx=5,sticky="news")
            tp.wait_variable(experimentMedium)
            var = StringVar()
            button = Button(tp, text="Set", command=lambda: var.set(1))
            button.grid(row=s,column=0,columnspan=s,sticky="news",ipady=5, ipadx = 5)
            button.wait_variable(var)
            sessionData["experiments"].append({"folder":os.path.relpath(experimentDir,dir),"name":experimentMedium.get(),"timestamp":str(datetime.datetime.now())})
            updateSessionData()
            tp.destroy()
            mover.send_custom_command("SDIR "+experimentDir)
            for pt in sessionData["points"]:
                mover.set_coordinates(Coordinate(pt["x"],pt["y"]))
                mover.send_custom_command(f"RUN {pt['filename']}")



pointList=[]
statusStr:StringVar=None

def generateIn(parentFrame):
    global experimentWidgets, preExperimentWidgets,statusStr
    statusStr=StringVar()
    title=Label(parentFrame,text="Capture",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    status=Label(parentFrame,textvariable=statusStr,font=TEXT_FONT)
    status.grid(row=1,column=0,columnspan=2)

    

    selectF=Button(parentFrame,text="Load environment", font=TEXT_FONT,command=selectSession)
    selectF.grid(row=2,column=0, padx=5)
    makeF=Button(parentFrame,text="Create environment", font=TEXT_FONT,command=createSession)
    makeF.grid(row=2,column=1, padx=5)
    preExperimentWidgets.append(selectF)
    preExperimentWidgets.append(makeF)
    preExperimentWidgets.append(pointRecord.parent)


    startB = Button(parentFrame,text="Launch experiment", font=TEXT_FONT, command=run)
    startB.grid(row=2,column=0, padx=5,sticky="news")
    startB.grid_remove()

    refD=Button(parentFrame,text=configuration.referenceNames[0]+" Ref", font=TEXT_FONT, command=lambda:takeReference(0))
    refD.grid(row=3,column=0, padx=5,sticky="news")
    refD.grid_remove()

    refB=Button(parentFrame,text=configuration.referenceNames[1]+ " Ref", font=TEXT_FONT, command=lambda:takeReference(1))
    refB.grid(row=3,column=1, padx=5,sticky="news")
    refB.grid_remove()

    refDB=Button(parentFrame,text=configuration.referenceNames[2]+ " Ref", font=TEXT_FONT, command=lambda:takeReference(2))
    refDB.grid(row=4,column=0,columnspan=2, padx=5,sticky="news")
    refDB.grid_remove()

    experimentWidgets.append(startB)
    experimentWidgets.append(refD)
    experimentWidgets.append(refB)
    experimentWidgets.append(refDB)

    

