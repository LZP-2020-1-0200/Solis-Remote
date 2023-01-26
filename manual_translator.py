
from modules.classes.coordinate import Coordinate
from modules.helpers import translator

SystemA:list[Coordinate]=[
    Coordinate(49311,-45811),
    Coordinate(58936,-35966),
    Coordinate(49137,-36065)
]
SystemB:list[Coordinate]=[
    Coordinate(0,0),
    Coordinate(0,-1),
    Coordinate(-1,0)
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
