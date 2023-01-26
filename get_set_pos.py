"""basic CLI for manual stage movement"""
from modules.classes import mover, Coordinate

mover.connect("COM6")

while True:
    inp:str=input("\'get\', \'set\', \'q\': ")
    if inp=="q":
        break
    if inp=="get":
        print(mover.get_coordinates())
    if inp=="set":
        mover.set_coordinates(Coordinate(int(input("X: ")),int(input("Y: "))))
