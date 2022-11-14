#Font constants for the app
TITLE_SIZE=30
TEXT_SIZE=20
_FONT="Arial"
TITLE_FONT=(_FONT,TITLE_SIZE)
TEXT_FONT=(_FONT,TEXT_SIZE)

mediums=[]
with open("./mediums.txt") as file:
    for line in file:
        mediums.append(line.rstrip())