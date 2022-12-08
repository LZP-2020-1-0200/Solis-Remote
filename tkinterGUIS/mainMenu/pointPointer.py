"""Generates the buttons to go to button and marker setup"""
from classes.event import CustomEvent
from tkinter import Button, Frame
from helpers.configuration import *
from tkinterGUIS import sessionData


onmovetoset:CustomEvent=CustomEvent()

onmovetoanchor:CustomEvent=CustomEvent()

set_points_button:Button|None=None
set_markers_button:Button|None=None

def _setPoints() -> None:
    onmovetoset()
def _setAnchors() -> None:
    onmovetoanchor()

def update_buttons() -> None:
    assert set_points_button is not None and set_markers_button is not None
    if sessionData.dataStruct.points_set:
        set_points_button["state"]="disabled"
    else:
        set_points_button["state"]="normal"
    if sessionData.dataStruct.local_anchors_set:
        set_markers_button["state"]="disable"
    else:
        set_markers_button["state"]="normal"

sessionData.onstatuschange.bind(update_buttons)

def generateIn(parent: Frame) -> None:
    global onmovetoset, onmovetoanchor, set_points_button, set_markers_button

    set_points_button=Button(parent,text="Set points",font=TEXT_FONT,command=_setPoints)
    set_points_button.grid(row=0,column=0)

    set_markers_button=Button(parent, text="Set anchors",font=TEXT_FONT,command=_setAnchors)
    set_markers_button.grid(row=1,column=0)



