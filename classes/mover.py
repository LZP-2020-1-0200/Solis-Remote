import time

import serial
import serial.tools.list_ports

from classes.coordinate import Coordinate
from classes.logger import Logger

logger = Logger(__name__).get_logger()

BAUDRATE = 9600


class MicroscopeMover:
    def __init__(self):
        self.serial: serial.Serial = serial.Serial()

    def connect(self, com_port: str) -> bool:

        if not com_port:
            logger.error("No COM port selected!")
            return False

        try:
            self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)
            logger.info(f"Successfully connected to {com_port}")

        except Exception as e:
            logger.error(e)
            return False

        self.set_speed()
        return True

    def get_coordinates(self) -> Coordinate:
        
        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b"\r").decode().split(",")[:2]
        cord = Coordinate(int(coord_string[0]), int(coord_string[1]))
        logger.info(f"Read point {cord}")
        return cord

    def set_coordinates(self, cord: Coordinate):
        logger.info(f"Going to: {cord.x} {cord.y}")
        string = f"G,{cord.x},{cord.y} \r"
        self.serial.write(string.encode())

        while self.serial.read_until(b"\r")[-2:] != b"R\r":
            time.sleep(0.05)

    def reset_coordinates(self):
        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)

    def set_speed(self, speed: int = 40):
        string = f"SMS,{speed} \r".encode()
        self.serial.write(string)

        while self.serial.read(2) != b"0\r":
            time.sleep(0.05)

        logger.info(f"Set speed to {speed}%")

    def close_connection(self):
        self.serial.close()
        logger.info("Closed connection")
    def send_custom_command(self, cmd):
        self.serial.write((cmd+"\r").encode("utf-8"))
        logger.info(f"Sent custom command: \"{cmd}\"")
        return self.serial.read_until(b"\r")


mover = MicroscopeMover()