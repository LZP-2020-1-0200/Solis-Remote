from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
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
import datetime;

sessionData={}
dir=None

def updateSessionData():
    global dir
    with open(dir+"/session.json", "w") as outfile:
        outfile.write(json.dumps(sessionData, indent=4))
        outfile.close()

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
    selectF.grid_forget()
    makeF.grid_forget()
    pointRecord.parent.grid_forget()
    startB.grid()
    

def createSession():
    global dir, sessionData
    dir=filedialog.askdirectory(title="Select directory of new session").replace("/","\\")
    sessionData=sessionSetup.sessionSetup(dir,pointList)
    selectF.grid_forget()
    makeF.grid_forget()
    pointRecord.parent.grid_forget()
    startB.grid()



def run():
    '''
    if not (dir == None):
        if connection.getStatus():
            
            saveable=[]
            i=1
            for pt in pointList:
                saveable.append({"x":pt[0],"y":pt[1],"filename":str(i).zfill(4)+".asc"})
                i+=1

            mover.send_custom_command("SDIR "+dir)
            i=1
            for pt in pointList:
                mover.set_coordinates(Coordinate(pt[0],pt[1]))
                mover.send_custom_command(f"RUN {i}.asc")
                i+=1
        else:
            print("Not connected.")
    else:
        print("no session selected")
    '''
    if not messagebox.askyesno("","Is SOLIS script on?"):
        return
    if connection.getStatus():
        global dir
        experimentDir=filedialog.askdirectory(title="Select directory of new experiment").replace("/","\\")

        if not (experimentDir==None):
            tp=Toplevel()
            experimentMedium=StringVar()
            for med in configuration.mediums:
                Radiobutton(tp, text = med, variable = experimentMedium,
                        value = med, indicator = 0,
                        background = "light blue").pack(fill=X, ipady = 5)
            tp.wait_variable(experimentMedium)
            var = StringVar()
            button = Button(tp, text="Set", command=lambda: var.set(1))
            button.pack(fill=X, ipady = 5)
            button.wait_variable(var)
            sessionData["experiments"].append({"folder":experimentDir,"name":experimentMedium.get(),"timestamp":str(datetime.datetime.now())})
            updateSessionData()
            tp.destroy()
            mover.send_custom_command("SDIR "+experimentDir)
            for pt in sessionData["points"]:
                mover.set_coordinates(Coordinate(pt["x"],pt["y"]))
                mover.send_custom_command(f"RUN {pt['filename']}")


selectF:Button=None
makeF:Button=None
startB:Button=None

pointList=[]

def generateIn(parentFrame):
    global selectF,makeF,startB
    title=Label(parentFrame,text="Capture",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    status=Label(parentFrame,text=f"Session: {dir}",font=TEXT_FONT)
    title.grid(row=1,column=0,columnspan=2)

    

    selectF=Button(parentFrame,text="Select environment", font=TEXT_FONT,command=selectSession)
    selectF.grid(row=2,column=0, padx=5)
    makeF=Button(parentFrame,text="Make environment", font=TEXT_FONT,command=createSession)
    makeF.grid(row=2,column=1, padx=5)

    startB = Button(parentFrame,text="Launch experiment", font=TEXT_FONT, command=run)
    startB.grid(row=2,column=2, padx=5)
    startB.grid_forget()

    

