#Font constants for the app
TITLE_SIZE=30
TEXT_SIZE=20
_FONT="Arial"
TITLE_FONT=(_FONT,TITLE_SIZE)
TEXT_FONT=(_FONT,TEXT_SIZE)

#media for experiments
media=[]
with open("./media_list.txt") as file:
    for line in file:
        media.append(line.rstrip())

#names of references
referenceNames=["dark","white","darkForWhite"]