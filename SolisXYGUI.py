import serial
from classes.coordinate import Coordinate
from classes.mover import mover
import time
# import tkinter module
from tkinter import * 
from tkinter import filedialog
from tkinterGUIS import setLoc
from tkinterGUIS import pointRecord
from tkinterGUIS import pointDisplay
from tkinterGUIS  import connection
from tkinterGUIS import sessionManager
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT








# creating main tkinter window/toplevel
master = Tk()
master.title("SolisXY GUI")
master.columnconfigure(tuple(range(60)), weight=1)
master.rowconfigure(tuple(range(30)), weight=1)

connectionFrame=Frame(master,bd=3,relief=SOLID)
connectionFrame.grid(row=0,column=0,sticky="news")
connection.generateIn(connectionFrame,mover)


#point recording GUI setup
ptRec=Frame(master,bd=3,relief=SOLID)
ptRec.grid(row=0,column=1,sticky="news")
pointRecord.generateIn(ptRec)


#point display GUI setup
ptDisp=Frame(master,bd=3,relief=SOLID)
ptDisp.grid(row=1,column=1,sticky="news")
pointDisplay.generateIn(ptDisp)

#frame for sessions and stage adjustments
sessionStageFrame=Frame(master,relief=SOLID)
sessionStageFrame.grid(row=1,column=0,sticky="news")

#Session loading GUI
CapFrame=Frame(sessionStageFrame,bd=1,relief=SOLID)
CapFrame.grid(row=0,column=0,sticky="news")
sessionManager.generateIn(CapFrame)

#Set location GUI setup TODO: remove when confirmed unnecessary
setLocationFrame=Frame(sessionStageFrame,bd=1,relief=SOLID)
setLocationFrame.grid(row=1,column=0,sticky="news")
setLoc.generateIn(setLocationFrame)




#updates all widths and heights for usage
master.update()



# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()