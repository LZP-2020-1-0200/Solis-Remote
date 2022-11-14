from tkinter import * 
from tkinterGUIS import connection
from classes.mover import mover
from classes.coordinate import Coordinate
from tkinterGUIS.configuration import TEXT_FONT
from tkinterGUIS.configuration import TITLE_FONT



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
    title=Label(parentFrame,text="Set stage location",font=TITLE_FONT)
    title.grid(row=0,column=0,columnspan=2)

    XLabel = Label(parentFrame, text = "X coordinate:",font=TEXT_FONT)
    YLabel = Label(parentFrame, text = "Y coordinate:",font=TEXT_FONT)


    XLabel.grid(row = 1, column = 0, sticky = W, pady = 5,padx=5)
    YLabel.grid(row = 2, column = 0, sticky = W, pady = 2,padx=5)

    vcmd = (parentFrame.register(validator),'%P')
    XEntry = Entry(parentFrame,font=TEXT_FONT, validate="key",validatecommand=vcmd)
    YEntry = Entry(parentFrame,font=TEXT_FONT, validate="key",validatecommand=vcmd)
    
    # this will arrange entry widgets
    XEntry.grid(row = 1, column = 1, padx=5, pady = 5)
    YEntry.grid(row = 2, column = 1, padx=5, pady = 5)
    
    def handleButton():
        setLocationHandler(int(XEntry.get()),int(YEntry.get()))

    moveButton = Button(parentFrame,text="Move Table", font=TEXT_FONT, command=handleButton)
    moveButton.grid(row=3,column=0, columnspan=2)