"""The main file that creates an application to use the microscope"""

from tkinter import Tk, Frame, mainloop
import logging

from modules.classes.scene_switcher import SceneSwitcher
from modules.classes.logger import Logger
from modules.guis import session_loader, connection, anchors
from modules.guis.PointRecording import point_record
from modules.guis.mainMenu import main_scene, set_switcher


log:logging.Logger=Logger(__name__).get_logger()

# creating main tkinter window/toplevel
master: Tk = Tk()
master.title("SolisXY GUI")
master.grid_rowconfigure(1, weight=1)
master.grid_columnconfigure(1, weight=1)

connection_frame: Frame=connection.GUI(master)
connection_frame.grid(row=0,column=0)

main_frame: Frame=Frame(master)
main_frame.grid(row=1,column=0)

main_switcher:SceneSwitcher=SceneSwitcher(main_frame)



session_load: int=main_switcher.add_scene()
session_loader.GUI(main_switcher.get_frame(session_load)).pack()

main_scene_id: int=main_switcher.add_scene()
main_scene.GUI(main_switcher.get_frame(main_scene_id)).pack()

point_scene: int=main_switcher.add_scene()
point_record.GUI(main_switcher.get_frame(point_scene)).pack()

anchor_scene: int=main_switcher.add_scene()
anchors.GUI(main_switcher.get_frame(anchor_scene)).pack()


# --- events ---

def to_point_reg() -> None:
    """Switches to the point registration scene"""
    main_switcher.switch_to(point_scene)
set_switcher.onmovetoset.bind(to_point_reg)

def to_anchor_reg() -> None:
    """Switches to the anchor registration scene"""
    main_switcher.switch_to(anchor_scene)
set_switcher.onmovetoanchor.bind(to_anchor_reg)


def to_main() -> None:
    """Switches to the main scene"""
    main_switcher.switch_to(main_scene_id)

session_loader.ontomenu.bind(to_main)
point_record.onsubmitpoints.bind(to_main)
anchors.onconfirmanchors.bind(to_main)

#updates all widths and heights for usage
master.update()


# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()
