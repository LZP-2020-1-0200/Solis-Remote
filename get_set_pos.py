"""basic CLI for manual stage movement"""
from modules.classes import MicroscopeMover, Coordinate, MicroscopeStatus


while True:
    inp:str=input("\'get\', \'set\', \'q\': ")
    with MicroscopeMover() as mover:
        if mover.last_status==MicroscopeStatus.CONNECTED:
            if inp=="q":
                break
            if inp=="get":
                print(mover.get_coordinates())
            if inp=="set":
                mover.set_coordinates(Coordinate(int(input("X: ")),int(input("Y: "))))
