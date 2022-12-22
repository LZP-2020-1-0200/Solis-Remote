from tkinter import Tk, Frame, mainloop
from classes.sceneSwitcher import SceneSwitcher
from tkinterGUIS import sessionLoader, connection, anchors
from tkinterGUIS.PointRecording import pointRecord
from tkinterGUIS.mainMenu import mainScene, setSwitcher
from classes.logger import Logger
import logging

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



session_loader: int=main_switcher.addScene()
sessionLoader.GUI(main_switcher.getFrame(session_loader)).pack()

main_scene: int=main_switcher.addScene()
mainScene.GUI(main_switcher.getFrame(main_scene)).pack()

point_scene: int=main_switcher.addScene()
pointRecord.GUI(main_switcher.getFrame(point_scene)).pack()

anchor_scene: int=main_switcher.addScene()
anchors.GUI(main_switcher.getFrame(anchor_scene)).pack()


# --- events ---



def toPointReg() -> None:
    main_switcher.switchTo(point_scene)
setSwitcher.onmovetoset.bind(toPointReg)

def toAnchorReg() -> None:
    main_switcher.switchTo(anchor_scene)
setSwitcher.onmovetoanchor.bind(toAnchorReg)


def toMain() -> None:
    main_switcher.switchTo(main_scene)

sessionLoader.ontomenu.bind(toMain)

pointRecord.onsubmitpoints.bind(toMain)

anchors.onconfirmanchors.bind(toMain)

#debug statements for event information
#pointRecord.onsubmitpoints.bind(lambda:log.debug("Points submitted."))
#sessionLoader.oncreate.bind(lambda:log.debug("Session loader create."))
#sessionLoader.onload.bind(lambda:log.debug("Session loader load."))
#setSwitcher.onmovetoset.bind(lambda:log.debug("Points set."))
#sessionData.onstatuschange.bind(lambda:log.debug("Status changed."))
#essionData.onpointchange.bind(lambda:log.debug("Points changed."))
#nchors.onconfirmanchors.bind(lambda:log.debug("Anchors confirmed"))


#updates all widths and heights for usage
master.update()


# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()
