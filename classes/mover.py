import time

import serial #type: ignore
import serial.tools.list_ports #type: ignore

from classes.coordinate import Coordinate
from classes.event import CustomEvent
from classes.logger import Logger
import logging
from typing import Literal
from enum import Enum

logger:logging.Logger = Logger(__name__).get_logger()

BAUDRATE: Literal[9600] = 9600

class MicroscopeStatus(Enum):
    SOLIS_UNRESPONSIVE  =1
    STAGE_UNRESPONSIVE  =2
    CONNECTED           =3
    DISCONNECTED        =4

class _MicroscopeMover:
    """
    A private class of the mover.py module instantiated only by `mover`
    """
    
    def __init__(self) -> None:
        self.serial: serial.Serial = serial.Serial()
        self.ontimeout:CustomEvent=CustomEvent()
        self.ontimeout.bind(lambda:logger.info("ontimeout called"))
        self.lastStatus:MicroscopeStatus=MicroscopeStatus.DISCONNECTED

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

        #test connection
        self.lastStatus=self._ping_all()
        if self.lastStatus==MicroscopeStatus.CONNECTED:
            self.set_speed(40)
            return True

        return False
    def _ping_all(self)->MicroscopeStatus:
        """Pings SOLIS and the stage to check the connection status. Does not close the connection."""
        
        logger.info("Checking port status")
        timeout:float=0.1
        if self.serial.is_open:
            previousTimeout:float|None=self.serial.timeout#type: ignore
            previousWriteTimeout:float|None=self.serial.write_timeout#type: ignore
            self.serial.timeout=timeout
            self.serial.write_timeout=timeout
            logger.info("Pinging SOLIS")
            self.serial.write(b"PING\r")#type: ignore
            response:str=self.serial.read_until(b"PING\r").decode("utf-8")#type:ignore

            
            # SOLIS is unresponsive
            if len(response)==0:
                logger.info("SOLIS unresponsive.")
                self.serial.write_timeout=previousWriteTimeout
                self.serial.timeout=previousTimeout
                return MicroscopeStatus.SOLIS_UNRESPONSIVE

            #SOLIS is responsive, check if stage responds
            self.serial.write(b"P \r")#type: ignore
            response=self.serial.read_until(b"\r").decode("utf-8")#type: ignore

            #Stage did not respond
            if len(response)==0:
                logger.info("Stage unresponsive")
                self.serial.write_timeout=previousWriteTimeout
                self.serial.timeout=previousTimeout
                return MicroscopeStatus.STAGE_UNRESPONSIVE


            #reset serial connection settings and send ok status
            self.serial.write_timeout=previousWriteTimeout
            self.serial.timeout=previousTimeout
            logger.info("Ping successful")
            return MicroscopeStatus.CONNECTED
        logger.info("Port is closed")
        return MicroscopeStatus.DISCONNECTED
    def ping(self)->MicroscopeStatus:
        """Pings SOLIS and the stage to check the connection status. Closes the connection if timeout is discovered"""

        # ping the stage only if it should be connected
        if self.lastStatus==MicroscopeStatus.CONNECTED:
            self.lastStatus:MicroscopeStatus=self._ping_all()

        # close the connection if something is unresponsive
        if self.lastStatus==MicroscopeStatus.SOLIS_UNRESPONSIVE or self.lastStatus==MicroscopeStatus.STAGE_UNRESPONSIVE:
            self.close_connection()
            self.ontimeout()# call timeout event
        
        return self.lastStatus

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
        logger.info("Resetting stage position")
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
        logger.info("Changing SOLIS output directory")
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

        logger.info("Capturing and saving in {filename}")
        self.serial.write(f"RUN {filename}\r".encode("utf-8"))#type: ignore
        self.serial.read_until(b"\r")#type: ignore
        pass

    def close_connection(self) -> None:
        """
        Closes the connection to the serial port
        """
        self.serial.close()
        logger.info("Connection terminated")

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