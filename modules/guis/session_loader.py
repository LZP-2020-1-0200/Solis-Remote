"""Responsible for GUI loading/creating sessions"""
from tkinter import Button, filedialog, Frame, Misc
import logging

from ..helpers.configuration import TEXT_FONT

from ..classes.event import CustomEvent
from ..classes import session_data
from ..classes.logger import Logger



log:logging.Logger=Logger(__name__).get_logger()



class GUI(Frame):
    """Generates a GUI of the switcher"""
    def __init__(self, parent:Misc) -> None:
        Frame.__init__(self, parent)
        select_env_button: Button=Button(self,
            text="Load environment",
            font=TEXT_FONT,
            command=self._select_session)
        select_env_button.grid(row=2,column=0, padx=5)
        make_env_button: Button=Button(self,
            text="Create environment",
            font=TEXT_FONT,
            command=self._create_session)
        make_env_button.grid(row=2,column=1, padx=5)
        log.info("GUI init")
        self.onload:CustomEvent=CustomEvent("session_loaderGUI.onload")
        self.oncreate:CustomEvent=CustomEvent("session_loaderGUI.oncreate")
        self.ontomenu:CustomEvent=CustomEvent("session_loaderGUI.ontomenu")

    def _select_session(self) -> None:
        """Prompts user to select session and loads data"""
        title:str='Select session directory'
        session_directory:str=filedialog.askdirectory(title=title).replace("/","\\")

        # check if directory was selected
        if session_directory=="":
            return

        session_data.data_struct.dir=session_directory
        session_data.load()
        self.onload()
        self.ontomenu()

    def _create_session(self) -> None:
        """Prompts user to select session and creates data"""
        title:str="Select directory of new session"
        session_directory: str=filedialog.askdirectory(title=title).replace("/","\\")

        #check if directory was selected
        if session_directory=="":
            return

        session_data.data_struct.dir=session_directory
        session_data.session_setup()
        session_data.load()
        self.oncreate()
        self.ontomenu()
    