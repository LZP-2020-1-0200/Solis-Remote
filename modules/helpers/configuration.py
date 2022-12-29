"""Loads and holds constants from configuration"""
from typing import Literal


#Font constants for the app
TITLE_SIZE: Literal[30]=30
TEXT_SIZE: Literal[20]=20
_FONT: Literal['Arial']="Arial"
TITLE_FONT: tuple[Literal['Arial'], Literal[30]]=(_FONT,TITLE_SIZE)
TEXT_FONT: tuple[Literal['Arial'], Literal[20]]=(_FONT,TEXT_SIZE)

#media for experiments
MEDIA:list[str]=[]
with open("./media_list.txt", encoding="utf-8") as file:
    for line in file:
        MEDIA.append(line.rstrip())

#names of references
REFERENCE_NAMES: list[str]=["dark","white","darkForWhite"]

BAUDRATE: Literal[9600] = 9600
