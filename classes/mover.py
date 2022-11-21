import time

import serial
import serial.tools.list_ports

from classes.coordinate import Coordinate
from classes.logger import Logger

logger = Logger(__name__).get_logger()

BAUDRATE = 9600


class _MicroscopeMover:
    """
    A private class of the mover.py module instantiated only by `mover`
    """

    def __init__(self):
        self.serial: serial.Serial = serial.Serial()

    def connect(self, com_port: str) -> bool:
        """
        Connects to the serial port `com_port`, returns whether connection has been established

        `com_port`: The port to which the mover should connect to e.g. `COM3`
        """

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

    def get_connection_state(self)->bool:
        """
        Returns whether mover is connected to a serial port
        """
        return self.serial.is_open

    def get_coordinates(self) -> Coordinate:
        """
        Returns the stage coordinates. 

        NOTE: this method does not check if the stage is moving and can return the coordinates while the stage is moving 
        """
        self.serial.write("P \r".encode())
        coord_string = self.serial.read_until(b"\r").decode().split(",")[:2]
        cord = Coordinate(int(coord_string[0]), int(coord_string[1]))
        logger.info(f"Read point {cord}")
        return cord

    def set_coordinates(self, cord: Coordinate)->None:
        """
        Sends a command to the stage to move to specific coordinates

        `cord`: The absolute coordinates to where should the stage be moved to
        """
        logger.info(f"Going to: {cord.x} {cord.y}")
        string = f"G,{cord.x},{cord.y} \r"
        self.serial.write(string.encode())

        while self.serial.read_until(b"\r")[-2:] != b"R\r":
            time.sleep(0.05)

    def reset_coordinates(self)->None:
        """
        Resets the stage to point (0,0)
        """
        self.serial.write(b"PS,0,0 \r")
        self.serial.read(2)
    
    def set_relative_coordinates(self,coord:Coordinate):
        """
        Moves the stage by `coord`
        Useful for tiny adjustments

        `coord`: the coordinates describing relative movement
        """
        logger.info(f"Moving by: {coord.x} {coord.y}")
        string = f"GR {coord.x},{coord.y} \r"
        self.serial.write(string.encode("utf-8"))
        self.serial.read_until(b"\r")


    def set_speed(self, speed: int = 40)->None:
        """
        Sets the speed of the stage

        `speed`: an integer corresponding to the speed
        """
        string = f"SMS,{speed} \r".encode()
        self.serial.write(string)

        #while self.serial.read(2) != b"0\r":
            #time.sleep(0.05)

        self.serial.read_until(b"\r")

        logger.info(f"Set speed to {speed}%")

    
    def set_output_directory(self,directory:str)->None:
        """
        Sends information to SOLIS script where to save future captures

        `directory`: Absolute path to where future saving should accur
        """
        #Change the target directory
        self.serial.write(f"SDIR {directory}\r".encode("utf-8"))
        #block until received response
        self.serial.read_until(b"\r")


    
    def take_capture(self,filename:str)->None:
        """
        Sends a command to SOLIS script to take an acquisition

        NOTE: It uses the acquisition settings set in the SOLIS software
        Files are saved in a directory set by `set_output_directory()`

        `filename`: the name of the file set
        """

        self.serial.write(f"RUN {filename}\r".encode("utf-8"))
        self.serial.read_until(b"\r")
        pass

    def close_connection(self):
        """
        Closes the connection to the serial port
        """
        self.serial.close()
        logger.info("Closed connection")

    def send_custom_command(self, cmd:bytes)->bytes:
        """
        Sends a custom command to the serial port and blocks until a response is received
        Returns the response without encoding

        NOTE: there is no need to add \\r to the end of the command

        `cmd`: The command that is sent to the SOLIS script
        """
        #send command
        self.serial.write(cmd+b"\r")

        logger.info(f"Sent custom command: \"{cmd}\"")

        #block until respnse received
        return self.serial.read_until(b"\r")


mover = _MicroscopeMover()
"""
The singleton instance of microscope mover.
Used for communication to the stage and SOLIS script
"""