from modules.classes.coordinate import Coordinate
from modules.helpers import translator

SystemA:list[Coordinate]=[
    Coordinate(0,0),
    Coordinate(0,2),
    Coordinate(2,2)
]
SystemB:list[Coordinate]=[
    Coordinate(-1,-3),
    Coordinate(-1,-5),
    Coordinate(-3,-5)
]
while True:
    print("Select mode\n1-from A to B\n2-from B to A\n3-exit")
    mode:int =int(input("Enter mode: "))
    if mode==3:
        break
    if mode==1 or mode==2:
        x:float=float(input("Enter X coordinate: "))
        y:float=float(input("Enter Y coordinate: "))
        c:Coordinate=Coordinate(x,y)
        if mode==1:
            print(translator.anchor_translate(SystemB,SystemA,c))
        if mode==2:
            print(translator.anchor_translate(SystemA,SystemB,c))
