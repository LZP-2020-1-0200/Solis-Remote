from tkinter import Tk, Frame, mainloop
from classes.sceneSwitcher import SceneSwitcher
from tkinterGUIS import sessionLoader, connection, sessionData, anchors
from tkinterGUIS.PointRecording import pointRecord
from tkinterGUIS.mainMenu import mainScene, pointPointer

# creating main tkinter window/toplevel
master: Tk = Tk()
master.title("SolisXY GUI")
master.grid_rowconfigure(1, weight=1)
master.grid_columnconfigure(1, weight=1)

connection_frame: Frame=Frame(master)
connection_frame.grid(row=0,column=0)
connection.generateIn(connection_frame)

main_frame: Frame=Frame(master)
main_frame.grid(row=1,column=0)

main_switcher:SceneSwitcher=SceneSwitcher(main_frame)



session_loader: int=main_switcher.addScene()
sessionLoader.generateIn(main_switcher.getFrame(session_loader))

main_scene: int=main_switcher.addScene()
mainScene.generateIn(main_switcher.getFrame(main_scene))

point_scene: int=main_switcher.addScene()
pointRecord.generateIn(main_switcher.getFrame(point_scene))

anchor_scene: int=main_switcher.addScene()
anchors.generateIn(main_switcher.getFrame(anchor_scene))


# --- events ---



def toPointReg() -> None:
    main_switcher.switchTo(point_scene)
pointPointer.onmovetoset.bind(toPointReg)

def toAnchorReg() -> None:
    main_switcher.switchTo(anchor_scene)
pointPointer.onmovetoanchor.bind(toAnchorReg)


def toMain() -> None:
    main_switcher.switchTo(main_scene)
#sessionLoader.onload.bind(toMain)
#sessionLoader.oncreate.bind(toMain)
sessionLoader.onToMenu.bind(toMain)

pointRecord.onsubmitpoints.bind(toMain)

anchors.onconfirmanchors.bind(toMain)

#debug statements for event information
pointRecord.onsubmitpoints.bind(lambda:print("Points submited."))
sessionLoader.oncreate.bind(lambda:print("Session loader create."))
sessionLoader.onload.bind(lambda:print("Session loader load."))
pointPointer.onmovetoset.bind(lambda:print("Points set."))
sessionData.onstatuschange.bind(lambda:print("Status changed."))
sessionData.onpointchange.bind(lambda:print("Points changed."))
anchors.onconfirmanchors.bind(lambda:print("Anchors confirmed"))


#updates all widths and heights for usage
master.update()


# infinite loop which can be terminated by keyboard
# or mouse interrupt
mainloop()
