"""Loads and holds constants from configuration"""
from typing import Literal


#Font constants for the app
TITLE_SIZE: int=24
TEXT_SIZE: int=16
_FONT: Literal['Arial']="Arial"
TITLE_FONT: tuple[Literal['Arial'], int]=(_FONT,TITLE_SIZE)
TEXT_FONT: tuple[Literal['Arial'], int]=(_FONT,TEXT_SIZE)

#media for experiments
MEDIA:list[str]=[]
with open("./media_list.txt", encoding="utf-8") as file:
    for line in file:
        MEDIA.append(line.rstrip())

#names of references
REFERENCE_NAMES: list[str]=["dark","white","darkForWhite"]

BAUDRATE: Literal[9600] = 9600
