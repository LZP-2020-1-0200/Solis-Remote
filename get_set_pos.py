from modules.classes.mover import mover
from modules.classes.coordinate import Coordinate

mover.connect("COM6")

while True:
    inp:str=input("\'get\', \'set\', \'q\': ")
    if inp=="q":
        break
    if inp=="get":
        print(mover.get_coordinates())
    if inp=="set":
        mover.set_coordinates(Coordinate(int(input("X: ")),int(input("Y: "))))
