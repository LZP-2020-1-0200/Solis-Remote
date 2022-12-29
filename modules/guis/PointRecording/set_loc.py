"""Contains GUI for relative movement of the stage"""
from tkinter import Frame, StringVar, Label, Button, Entry, Misc
from typing import Literal
import logging
from ...guis import connection
from ...classes.mover import mover
from ...classes.coordinate import Coordinate
from ...classes.logger import Logger

from ...helpers.configuration import TEXT_FONT
from ...helpers.configuration import TITLE_FONT



BUTTON_FONT: tuple[Literal['Arial'], Literal[25]]=("Arial", 25)

log:logging.Logger=Logger(__name__).get_logger()

class GUI(Frame):
    """Creates a GUI for relative movement for the stage"""
    def __init__(self,parent:Misc) -> None:
        Frame.__init__(self,parent)
        self._step_str_var: StringVar=StringVar()

        title: Label=Label(self,text="Move stage",font=TITLE_FONT)
        title.grid(row=0,column=0,columnspan=2)

        button_frame: Frame=Frame(self)
        button_frame.grid(row=1,column=0,columnspan=2)
        Button(button_frame,text="🢄",font=BUTTON_FONT,
            command=lambda: self._rel_move(-1,-1)).grid(row=1,column=0,sticky="news")
        Button(button_frame,text="🢁",font=BUTTON_FONT,
            command=lambda: self._rel_move(0,-1)).grid(row=1,column=1,sticky="news")
        Button(button_frame,text="🢅",font=BUTTON_FONT,
            command=lambda: self._rel_move(1,-1)).grid(row=1,column=2,sticky="news")
        Button(button_frame,text="🢀",font=BUTTON_FONT,
            command=lambda: self._rel_move(-1,0)).grid(row=2,column=0,sticky="news")
        Button(button_frame,text="🢂",font=BUTTON_FONT,
            command=lambda: self._rel_move(1,0)).grid(row=2,column=2,sticky="news")
        Button(button_frame,text="🢇",font=BUTTON_FONT,
            command=lambda: self._rel_move(-1,1)).grid(row=3,column=0,sticky="news")
        Button(button_frame,text="🢃",font=BUTTON_FONT,
            command=lambda: self._rel_move(0,1)).grid(row=3,column=1,sticky="news")
        Button(button_frame,text="🢆",font=BUTTON_FONT,
            command=lambda: self._rel_move(1,1)).grid(row=3,column=2,sticky="news")


        step_label: Label = Label(self, text = "Step (in μm):",font=TEXT_FONT)
        step_label.grid(row = 4, column = 0, sticky = 'w', pady = 5,padx=5)

        vcmd: tuple[str, Literal['%P']] = (self.register(self._validator),'%P')

        step_entry: Entry = Entry(self,font=TEXT_FONT, validate="key",
            validatecommand=vcmd,textvariable=self._step_str_var)
        self._step_str_var.set("10")
        step_entry.grid(row = 4, column = 1, padx=5, pady = 5)
        log.info("GUI init")

    def _rel_move(self,x_coord:int,y_coord:int)->None:
        """Moves the stage by x and y"""
        relative_coord: Coordinate=Coordinate(x_coord,y_coord)*int(self._step_str_var.get())
        if connection.get_status():
            mover.set_relative_coordinates(relative_coord)


    def _set_location_handler(self,x_coord:int,y_coord:int) -> None:
        if connection.get_status():
            mover.set_coordinates(Coordinate(x_coord,y_coord))
        else:
            print("Not connected.")

    def _validator(self,value_if_allowed:str) -> bool:
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
