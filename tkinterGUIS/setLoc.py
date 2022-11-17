from tkinter import * 
from tkinterGUIS import connection
from classes.mover import mover
from classes.coordinate import Coordinate
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT

stepValue:StringVar=None

def relMove(x,y):
    c=Coordinate(x,y)*int(stepValue.get())
    if connection.getStatus():
        nc=mover.get_coordinates()+c
        mover.set_coordinates(nc)
    pass

def setLocationHandler(x,y):
    if connection.getStatus():
        mover.set_coordinates(Coordinate(x,y))
    else:
        print("Not connected.")



def validator(value_if_allowed):
    #check for empty string
    if value_if_allowed=='' or value_if_allowed=='-':
        return True
    #deny spaces
    if ' ' in value_if_allowed:
        return False

    #test if is convertible to int
    try:
        int(value_if_allowed)
        return True
    except ValueError:
        return False
#generates the set location GUI in parentFrame with font settings. callback will be called with parameters (x,y)
def generateIn(parentFrame):
    global stepValue
    stepValue=StringVar()

    title=Label(parentFrame,text="Move stage",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    butFrame=Frame(parentFrame)
    butFrame.grid(row=1,column=0,columnspan=2)
    
    buttonFont=("Arial", 25)
    Button(butFrame,text="🢄",font=buttonFont,command=lambda: relMove(-1,-1)).grid(row=1,column=0,sticky="news")
    Button(butFrame,text="🢁",font=buttonFont,command=lambda: relMove(0,-1)).grid(row=1,column=1,sticky="news")
    Button(butFrame,text="🢅",font=buttonFont,command=lambda: relMove(1,-1)).grid(row=1,column=2,sticky="news")
    Button(butFrame,text="🢀",font=buttonFont,command=lambda: relMove(-1,0)).grid(row=2,column=0,sticky="news")
    Button(butFrame,text="🢂",font=buttonFont,command=lambda: relMove(1,0)).grid(row=2,column=2,sticky="news")
    Button(butFrame,text="🢇",font=buttonFont,command=lambda: relMove(-1,1)).grid(row=3,column=0,sticky="news")
    Button(butFrame,text="🢃",font=buttonFont,command=lambda: relMove(0,1)).grid(row=3,column=1,sticky="news")
    Button(butFrame,text="🢆",font=buttonFont,command=lambda: relMove(1,1)).grid(row=3,column=2,sticky="news")
    

    stepLabel = Label(parentFrame, text = "Step",font=TEXT_FONT)
    stepLabel.grid(row = 4, column = 0, sticky = W, pady = 5,padx=5)

    vcmd = (parentFrame.register(validator),'%P')

    stepEntry = Entry(parentFrame,font=TEXT_FONT, validate="key",validatecommand=vcmd,textvariable=stepValue)
    stepValue.set("10")
    stepEntry.grid(row = 4, column = 1, padx=5, pady = 5)

