import time

import serial #type: ignore
import serial.tools.list_ports #type: ignore

from classes.coordinate import Coordinate
from classes.event import CustomEvent
from classes.logger import Logger
import logging
from typing import Literal

logger:logging.Logger = Logger(__name__).get_logger()

BAUDRATE: Literal[9600] = 9600


class _MicroscopeMover:
    """
    A private class of the mover.py module instantiated only by `mover`
    """

    def __init__(self) -> None:
        self.serial: serial.Serial = serial.Serial()
        self.ontimeout:CustomEvent=CustomEvent()

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

        self.set_speed(40)
        return True

    def ping(self)->bool:
        """Pings SOLIS to check the connection status"""
        if self.serial.is_open:
            previousTimeout:float|None=self.serial.timeout#type: ignore
            previousWriteTimeout:float|None=self.serial.write_timeout#type: ignore
            self.serial.timeout=0.2
            self.serial.write_timeout=0.2
            self.serial.write(b"PING\r")#type: ignore
            response:str=self.serial.read_until(b"PING\r").decode("utf-8")#type:ignore

            self.serial.write_timeout=previousWriteTimeout
            self.serial.timeout=previousTimeout
            
            if len(response)==0:
                self.close_connection()
                self.ontimeout()# call timeout event
                return False
            return True
        return False


    def get_connection_state(self)->bool:
        """
        Returns whether mover is connected to a serial port
        """
        self.ping()
        return self.serial.is_open

    def get_coordinates(self) -> Coordinate:
        """
        Returns the stage coordinates. 

        NOTE: this method does not check if the stage is moving and can return the coordinates while the stage is moving 
        """


        self.serial.write("P \r".encode())#type: ignore
        coord_string: list[str] = self.serial.read_until(b"\r").decode().split(",")[:2]#type: ignore
        cord: Coordinate = Coordinate(int(coord_string[0]), int(coord_string[1]))
        logger.info(f"Read point {cord}")
        return cord

    def set_coordinates(self, cord: Coordinate)->None:
        """
        Sends a command to the stage to move to specific coordinates

        `cord`: The absolute coordinates to where should the stage be moved to
        returns True if successful
        """
        logger.info(f"Going to: {cord.x} {cord.y}")
        string: str = f"G,{cord.x},{cord.y} \r"
        self.serial.write(string.encode())#type: ignore

        while self.serial.read_until(b"\r")[-2:] != b"R\r":#type: ignore
            time.sleep(0.05)
    def reset_coordinates(self)->None:
        """
        Resets the stage to point (0,0)
        """
        self.serial.write(b"PS,0,0 \r")#type: ignore
        self.serial.read(2)
    
    def set_relative_coordinates(self,coord:Coordinate) -> None:
        """
        Moves the stage by `coord`
        Useful for tiny adjustments

        `coord`: the coordinates describing relative movement
        """


        logger.info(f"Moving by: {coord.x} {coord.y}")
        string: str = f"GR {coord.x},{coord.y} \r"
        self.serial.write(string.encode("utf-8"))#type: ignore
        self.serial.read_until(b"\r")#type: ignore


    def set_speed(self, speed: int = 40)->None:
        """
        Sets the speed of the stage

        `speed`: an integer corresponding to the speed
        """
        string: bytes = f"SMS,{speed} \r".encode()
        self.serial.write(string)#type: ignore

        #while self.serial.read(2) != b"0\r":
        #    time.sleep(0.05)

        self.serial.read_until(b"\r")#type: ignore

        logger.info(f"Set speed to {speed}%")

    
    def set_output_directory(self,directory:str)->None:
        """
        Sends information to SOLIS script where to save future captures

        `directory`: Absolute path to where future saving should accur
        """
        #Change the target directory
        self.serial.write(f"SDIR {directory}\r".encode("utf-8"))#type: ignore
        #block until received response
        self.serial.read_until(b"\r")#type: ignore


    
    def take_capture(self,filename:str)->None:
        """
        Sends a command to SOLIS script to take an acquisition

        NOTE: It uses the acquisition settings set in the SOLIS software
        Files are saved in a directory set by `set_output_directory()`

        `filename`: the name of the file set
        """

        self.serial.write(f"RUN {filename}\r".encode("utf-8"))#type: ignore
        self.serial.read_until(b"\r")#type: ignore
        pass

    def close_connection(self) -> None:
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
        self.serial.write(cmd+b"\r")#type: ignore

        logger.info(f"Sent custom command: \"{cmd}\"")

        #block until respnse received
        return self.serial.read_until(b"\r")#type: ignore


mover: _MicroscopeMover = _MicroscopeMover()
"""
The singleton instance of microscope mover.
Used for communication to the stage and SOLIS script
"""