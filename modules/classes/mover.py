"""Contains the class responsible for connecting to SOLIS and stage control"""
import time
import logging
from typing import Callable
from enum import Enum
import serial #type: ignore
import serial.tools.list_ports #type: ignore

from .coordinate import Coordinate
from .event import CustomEvent
from .logger import Logger
from ..helpers.configuration import BAUDRATE, LOOPBACK_A

logger:logging.Logger = Logger(__name__).get_logger()



class MicroscopeStatus(Enum):
    """Enum of possible microscope connection statuses"""
    SOLIS_UNRESPONSIVE  =1
    STAGE_UNRESPONSIVE  =2
    CONNECTED           =3
    DISCONNECTED        =4

class MicroscopeMover:
    """
    A singleton class of the mover.py module instantiated only by `mover`
    Does not ensure that a connection is there.
    May block endlessly if messages are sent to a severed connection
    """

    __instance:'MicroscopeMover|None'=None

    ontimeout:CustomEvent=CustomEvent("MicroscopeMover.ontimeout")
    ondisconnect:CustomEvent=CustomEvent("MicroscopeMover.ondisconnect")
    onsolisunresponsive:CustomEvent=CustomEvent("MicroscopeMover.onsolisunresponsive")
    onstageunresponsive:CustomEvent=CustomEvent("MicroscopeMover.onstageunresponsive")
    onconnect:CustomEvent=CustomEvent("MicroscopeMover.onconnect")

    def __init__(self) -> None:
        if MicroscopeMover.__instance is None:
            MicroscopeMover.__instance=self
            self.serial: serial.Serial = serial.Serial()
            self.last_status:MicroscopeStatus=MicroscopeStatus.DISCONNECTED
        else:
            try:
                raise Exception("Creating new instances of MicroscopeMover is forbidden")
            finally:
                logger.error("An attempt at creating a new MicroscopeMover instance was made")

    @staticmethod
    def converse(
            callback:'Callable[[MicroscopeMover], None]') -> MicroscopeStatus:
        """Attempts to connect to the stage and SOLIS, if successful,
        calls `callback`.

        To supply more parameters to the target function,
        encapsulate the target function in a lambda e.g.
        `MicroscopeMover.converse(lambda mover:target_function(mover, ...))`
        """
        micro_m: MicroscopeMover
        if MicroscopeMover.__instance is not None:
            micro_m = MicroscopeMover.__instance
        else:
            micro_m = MicroscopeMover()
        if micro_m.connect(LOOPBACK_A):
            logger.info("Converse start.")
            callback(micro_m)
            logger.info("Converse end.")
            micro_m.close_connection()
            return MicroscopeStatus.CONNECTED
        return micro_m.ping()


    def connect(self, com_port: str) -> bool:
        """
        Connects to the serial port `com_port`, returns whether connection has been established
        `com_port`: The port to which the mover should connect to e.g. `COM3`
        """

        if not com_port:
            logger.warning("No COM port selected!")
            return False

        # Attempt connection
        try:
            self.serial = serial.Serial(port=com_port, baudrate=BAUDRATE)
            logger.info("Successfully connected to %s", com_port)

        except serial.SerialException as exception:
            logger.error(exception)
            MicroscopeMover.ondisconnect()
            return False
        except ValueError as exception:
            logger.error(exception)
            return False

        #test connection
        self.last_status=self._ping_all()
        if self.last_status==MicroscopeStatus.CONNECTED:
            self.set_speed(40)
            return True

        return False
    def _ping_all(self)->MicroscopeStatus:
        """
        Pings SOLIS and the stage to check the connection status.
        Does not close the connection.
        """

        logger.info("Checking port status")
        timeout:float=0.3
        if self.serial.is_open:
            previous_timeout:float|None=self.serial.timeout#type: ignore
            previous_write_timeout:float|None=self.serial.write_timeout#type: ignore
            self.serial.timeout=timeout
            self.serial.write_timeout=timeout
            logger.info("Pinging SOLIS")
            self.serial.write(b"PING\r")#type: ignore
            response:str=self.serial.read_until(b"PING\r").decode("utf-8").strip()#type:ignore

            # SOLIS is unresponsive
            if len(response)==0:
                logger.info("SOLIS unresponsive.")
                MicroscopeMover.onsolisunresponsive()
                self.serial.write_timeout=previous_write_timeout
                self.serial.timeout=previous_timeout
                return MicroscopeStatus.SOLIS_UNRESPONSIVE

            #SOLIS is responsive, check if stage responds
            self.serial.write(b"SERIAL\r")#type: ignore
            response: str=self.serial.read_until(b"\r").decode('utf-8').rstrip()#type: ignore
            if not response.isnumeric():
                logger.info("Stage unresponsive")
                MicroscopeMover.onstageunresponsive()
                self.serial.write_timeout=previous_write_timeout
                self.serial.timeout=previous_timeout
                return MicroscopeStatus.STAGE_UNRESPONSIVE

            #reset serial connection settings and send ok status
            self.serial.write_timeout=previous_write_timeout
            self.serial.timeout=previous_timeout
            MicroscopeMover.onconnect()
            logger.info("Ping successful")
            return MicroscopeStatus.CONNECTED
        logger.info("Port is closed")
        MicroscopeMover.ondisconnect()
        return MicroscopeStatus.DISCONNECTED
    def ping(self)->MicroscopeStatus:
        """Pings SOLIS and the stage to check the connection status.
        Closes the connection if timeout is discovered.
        """

        # ping the stage only if it should be connected
        if self.last_status==MicroscopeStatus.CONNECTED:
            self.last_status=self._ping_all()

        # close the connection if something is unresponsive
        if (    self.last_status==MicroscopeStatus.SOLIS_UNRESPONSIVE or
                self.last_status==MicroscopeStatus.STAGE_UNRESPONSIVE):
            self.close_connection()
            self.ontimeout()# call timeout event

        return self.last_status

    def get_coordinates(self) -> Coordinate:
        """
        Returns the stage coordinates.

        NOTE: this method does not check if the stage is moving
        and can return the coordinates while the stage is in motion
        """
        self.serial.write("P \r".encode())#type: ignore
        coord_string: list[str] = self.serial.read_until(b"\r").decode().split(",")[:2]#type: ignore
        coord: Coordinate = Coordinate(int(coord_string[0]), int(coord_string[1]))
        logger.info("Read point %s",coord)
        return coord

    def set_coordinates(self, coord: Coordinate)->None:
        """
        Sends a command to the stage to move to specific coordinates

        `cord`: The absolute coordinates to where should the stage be moved to
        returns True if successful
        """
        rounded_coord: Coordinate=coord.rounded()
        logger.info("Going to: %i, %i", rounded_coord.x, rounded_coord.y)
        string: str = f"G,{rounded_coord.x},{rounded_coord.y} \r"
        self.serial.write(string.encode())#type: ignore

        #wait until stage reaches it's destination
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


        logger.info("Moving by: %i, %i", coord.x, coord.y)
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
        self.serial.read_until(b"\r")#type: ignore

        logger.info("Set speed to %i%%", speed)

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

        logger.info("Capturing and saving in %s", filename)
        self.serial.write(f"RUN {filename}\r".encode("utf-8"))#type: ignore
        self.serial.read_until(b"\r")#type: ignore

    def close_connection(self) -> None:
        """
        Closes the connection to the serial port
        """
        self.serial.close()
        logger.info("Connection terminated")

    def send_custom_command(self, cmd:bytes)->bytes:
        """
        Sends a custom command to the serial port and blocks until a response is received
        Returns the response without encoding.

        Warning: Use with caution!
        This is meant for developing new functionality and not for production.

        NOTE: there is no need to add \\r to the end of the command

        `cmd`: The command that is sent to the SOLIS script
        """
        #send command
        self.serial.write(cmd+b"\r")#type: ignore

        # custom commands should not be used, this is logged as an error
        logger.error("Sent custom command: \"%s\"", cmd)

        #block until respnse received
        return self.serial.read_until(b"\r")#type: ignore
