"""The main file that creates an application to use the microscope"""

from tkinter import Tk, Frame, mainloop, messagebox
import logging

from modules.classes.scene_switcher import SceneSwitcher
from modules.classes.logger import Logger
from modules.guis import session_loader, connection, anchors
from modules.guis.PointRecording import point_record
from modules.guis.mainMenu import main_scene
from modules.helpers.configuration import (
    STAGE_EXISTS, LOOPBACK_EXISTS,
    LOOPBACK_A, LOOPBACK_B,
    STAGE_PORT
    )


log:logging.Logger=Logger(__name__).get_logger()

#Check if ports found
if not STAGE_EXISTS:
    messagebox.showwarning("Automated port location error!", #type:ignore
        "Stage controller port not found!\n"+
        "If you wish to control the stage, fix your connection and restart this program.")
if not LOOPBACK_EXISTS:
    messagebox.showwarning("Automated port location error!", #type:ignore
        "Serial loopback connection not found!\n"+
        "If you wish to connect to SOLIS, fix your connection and restart the program.")

#set up the config file for SOLIS
with open("./SOLIS.cfg","w",encoding='utf-8') as f:
    f.write(f"STAGE_PORT\n{STAGE_PORT[3:]}\nAPP_PORT\n{LOOPBACK_B[3:]}\nEND")
log.info("Ports set. Loopback ports: %s and %s, Stage port: %s", LOOPBACK_A, LOOPBACK_B, STAGE_PORT)


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
session_loader_gui:session_loader.GUI=session_loader.GUI(main_switcher.get_frame(session_load))
session_loader_gui.pack()

main_scene_id: int=main_switcher.add_scene()
main_scene_gui:main_scene.GUI=main_scene.GUI(main_switcher.get_frame(main_scene_id))
main_scene_gui.pack()

point_scene: int=main_switcher.add_scene()
point_record_gui:point_record.GUI=point_record.GUI(main_switcher.get_frame(point_scene))
point_record_gui.pack()

anchor_scene: int=main_switcher.add_scene()
anchor_gui:anchors.GUI=anchors.GUI(main_switcher.get_frame(anchor_scene))
anchor_gui.pack()


# --- events ---

def to_point_reg() -> None:
    """Switches to the point registration scene"""
    main_switcher.switch_to(point_scene)
main_scene_gui.set_switcher.onmovetoset.bind(to_point_reg)

def to_anchor_reg() -> None:
    """Switches to the anchor registration scene"""
    main_switcher.switch_to(anchor_scene)
main_scene_gui.set_switcher.onmovetoanchor.bind(to_anchor_reg)


def to_main() -> None:
    """Switches to the main scene"""
    main_switcher.switch_to(main_scene_id)

session_loader_gui.ontomenu.bind(to_main)
point_record_gui.onsubmitpoints.bind(to_main)
point_record_gui.oncancelpointselection.bind(to_main)
anchor_gui.onconfirmanchors.bind(to_main)
anchor_gui.oncancelanchors.bind(to_main)

#updates all widths and heights for usage
master.update()


# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()
