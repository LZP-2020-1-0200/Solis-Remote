"""Contains a scene switching class for easier menu swapping"""
import logging
from tkinter import Misc, Frame
from .logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

class SceneSwitcher():
    """Contains references to frames and functionallity to switch between them
    by hiding/unhiding them
    """
    def __init__(self, parent:Misc) -> None:
        self._scenes:list[Frame]=[]
        self._parent:Misc=parent

    def add_scene(self)->int:
        """Adds a new `Frame` to the scene,
        returns the inner id of the created Frame
        """
        scene:Frame=Frame(self._parent)
        self._scenes.append(scene)
        if len(self._scenes)==1:
            scene.pack()
        return len(self._scenes)-1

    def get_frame(self,scene_id:int)->Frame:
        """Returns a reference to the frame with inner id `scene_id`"""
        return self._scenes[scene_id]

    def switch_to(self, scene_id:int)->None:
        """Switches to the frame with inner id `scene_id`"""
        for scene in self._scenes:
            scene.pack_forget()
        self._scenes[scene_id].pack()
        log.info("Switching to scene [%i]", scene_id)
        