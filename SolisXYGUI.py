import serial
import time
from tkinter import * 

#imports from classes
from classes.coordinate import Coordinate
from classes.mover import mover

#acquires default fonts from config
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT


#GUI modules
from tkinterGUIS import setLoc
from tkinterGUIS import pointRecord
from tkinterGUIS import pointDisplay
from tkinterGUIS  import connection
from tkinterGUIS import sessionManager


# creating main tkinter window/toplevel
master = Tk()
master.title("SolisXY GUI")
master.columnconfigure(tuple(range(60)), weight=1)
master.rowconfigure(tuple(range(30)), weight=1)



#connection GUI setup (./tkinterGUIS/connection.py)
connectionFrame=Frame(master,bd=3,relief=SOLID)
connectionFrame.grid(row=0,column=0,sticky="news")
connection.generateIn(connectionFrame)


#point recording GUI setup (./tkinterGUIS/pointRecord.py)
ptRec=Frame(master,bd=3,relief=SOLID)
ptRec.grid(row=0,column=1,sticky="news")
pointRecord.generateIn(ptRec)


#point display GUI setup (./tkinterGUIS/pointDisplay.py)
ptDisp=Frame(master,bd=3,relief=SOLID)
ptDisp.grid(row=1,column=1,sticky="news")
pointDisplay.generateIn(ptDisp)

#frame for sessions and stage adjustments 
sessionStageFrame=Frame(master,relief=SOLID)
sessionStageFrame.grid(row=1,column=0,sticky="news")

#Session loading GUI (./tkinterGUIS/sessionManager.py)
capFrame=Frame(sessionStageFrame,bd=1,relief=SOLID)
capFrame.grid(row=0,column=0,sticky="ns")
capFrame.columnconfigure(0,weight=1, uniform='third')
capFrame.columnconfigure(1,weight=1, uniform='third')
sessionManager.generateIn(capFrame)

#GUI for manual stage movement (./tkinterGUIS/setLoc.py)
setLocationFrame=Frame(sessionStageFrame,bd=1,relief=SOLID)
setLocationFrame.grid(row=1,column=0,sticky="news")
setLoc.generateIn(setLocationFrame)


#updates all widths and heights for usage
master.update()


# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()