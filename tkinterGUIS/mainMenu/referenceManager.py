from tkinter import Label, Button, Widget

from helpers.configuration import *
from tkinterGUIS.mainMenu import sessionManager


def generateIn(parent:Widget) -> None:

    label: Label=Label(parent, text="References",font=TITLE_FONT)
    label.grid(row=0,column=0,columnspan=2)

    refD: Button=Button(parent,text=referenceNames[0]+" Ref", font=TEXT_FONT, command=lambda:sessionManager.takeReference(0))
    refD.grid(row=3,column=0, padx=5,sticky="news")

    refB: Button=Button(parent,text=referenceNames[1]+ " Ref", font=TEXT_FONT, command=lambda:sessionManager.takeReference(1))
    refB.grid(row=3,column=1, padx=5,sticky="news")

    refDB: Button=Button(parent,text=referenceNames[2]+ " Ref", font=TEXT_FONT, command=lambda:sessionManager.takeReference(2))
    refDB.grid(row=4,column=0,columnspan=2, padx=5,sticky="news")
