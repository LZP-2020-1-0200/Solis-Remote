"""Loads and holds constants from configuration"""
from typing import Literal
from .port_finder import find_loop_back_or_default, find_stage_or_default

#Font constants for the app
TITLE_SIZE: int=24
TEXT_SIZE: int=16
_FONT: Literal['Arial']="Arial"
TITLE_FONT: tuple[Literal['Arial'], int]=(_FONT,TITLE_SIZE)
TEXT_FONT: tuple[Literal['Arial'], int]=(_FONT,TEXT_SIZE)

#media for experiments
_media:list[str]=[]
def reload_media() -> None:
    """Fetches the environments from media_list.txt"""
    _media.clear()
    with open("./media_list.txt", encoding="utf-8") as file:
        for line in file:
            _media.append(line.rstrip())

def get_media() -> list[str]:
    """Returns currently loaded media"""
    return _media

reload_media()

#names of references
REFERENCE_NAMES: list[str]=["dark","white","darkForWhite"]

BAUDRATE: Literal[9600] = 9600

#locate stage and Loopback ports
_loop_back:tuple[bool,str,str]=find_loop_back_or_default()
LOOPBACK_EXISTS: bool=_loop_back[0]
LOOPBACK_A:str= _loop_back[1]
"""Port that the app connects to for connection with SOLIS"""
LOOPBACK_B:str= _loop_back[2]
"""Port that SOLIS connects to for connection with the app. To be written to SOLIS.cfg"""

_stage_port: tuple[bool, str]=find_stage_or_default()
STAGE_EXISTS:bool=_stage_port[0]
STAGE_PORT:str=_stage_port[1]
"""Port that SOLIS connects to for connection with the stage controller.
To be written to SOLIS.cfg
"""
