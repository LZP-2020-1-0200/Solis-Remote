"""Functions for locating loopback and stage ports"""
import logging
import serial #type: ignore
import serial.tools.list_ports #type: ignore

from ..classes.logger import Logger


log:logging.Logger=Logger(__name__).get_logger()

def get_com_ports() -> list[str]:
    """Returns a list of all COM ports"""
    return [item.name for item in list(serial.tools.list_ports.comports())]#type:ignore

def find_loop_back() -> tuple[bool,str,str]:
    """Returns a tuple containing a bool that denotes if location was successful,
    and the 2 ports that are connected to each other.
    """
    port_a: serial.Serial=serial.Serial()
    port_b: serial.Serial=serial.Serial()
    timeout:float=0.1
    port_a.timeout=timeout
    port_b.timeout=timeout
    port_a.write_timeout=timeout
    port_b.write_timeout=timeout
    available_ports:list[str]=get_com_ports()
    for ind, port_name_a in enumerate(available_ports[:-1]):
        for port_name_b in available_ports[ind+1:]:
            try:
                port_a.setPort(port_name_a)#type:ignore
                port_b.setPort(port_name_b)#type:ignore
                port_a.open()
                port_b.open()
                port_b.read_all()
                test_string:str="TEST_123\r"
                port_a.write(test_string.encode('utf-8'))#type:ignore
                response: bytes=port_b.read_until(b"\r")#type:ignore
                if response.decode('utf-8')==test_string:
                    return True, port_name_a, port_name_b
                port_a.close()
                port_b.close()
            except serial.SerialException:
                continue

    return False, "",""

def find_stage() -> tuple[bool, str]:
    """Returns a tuple of a bool that denotes if the stage port was successfuly found
    and the port name
    Can be wrong if SOLIS is tunnelling to it
    """
    port:serial.Serial=serial.Serial()
    available_ports:list[str]=get_com_ports()
    timeout:float=0.1
    port.timeout=timeout
    port.write_timeout=timeout
    for port_name in available_ports:
        port.setPort(port_name)#type: ignore
        try:
            port.open()
            port.read_all()
            port.write(b"SERIAL\r")#type: ignore
            response: str=port.read_until(b"\r").decode('utf-8').rstrip()#type: ignore
            if response.isnumeric():
                return True, port_name
            port.close()
        except serial.SerialException:
            continue
    return False, ''

def find_stage_or_default() -> tuple[bool, str]:
    """Finds the stage port and checks if it isn't SOLIS in disguise.
    Returns True in the bool if it's found successfully,
    False, if neither stage port nor default port were found
    """
    is_solis_blocking_ports:bool=False
    stage_found_automatically:bool
    found_port:str
    stage_found_automatically,found_port=find_stage()
    if stage_found_automatically:
        #we need to make sure it is the stage and not SOLIS forwarding the port
        ser_port:serial.Serial=serial.Serial(found_port)
        ser_port.write_timeout=0.1
        ser_port.timeout=0.1
        ser_port.read_all()
        # When writing "PING\r", the stage will respond with R (default behaviour),
        # but SOLIS would capture that command and return "PING\r"
        ser_port.write(b"PING\r")#type: ignore
        response:str=ser_port.read_until(b"\r").decode('utf-8').rstrip()#type: ignore
        if response!="R":
            is_solis_blocking_ports=True
        ser_port.close()
    #if the stage port is blocked, return what is found on config file
    if not stage_found_automatically or is_solis_blocking_ports:
        with open("./SOLIS.cfg","r",encoding='utf-8') as file:
            line:str=""
            for line in file:
                line=line.rstrip()
                if line=="STAGE_PORT":
                    line=file.readline()
                    return True, "COM"+line.rstrip()
            return False, ""
    else:
        return True, found_port

def find_loop_back_or_default() -> tuple[bool, str, str]:
    """Locates loopback ports or defaults to previously found ports,
    bool is True if loopback was found,
    False if neither valid ports nor a default ports were found
    """
    is_loop_back_found:bool
    lp_port_a:str=""
    lp_port_b:str=""

    is_loop_back_found, lp_port_a, lp_port_b=find_loop_back()
    if not is_loop_back_found:
        is_a_found:bool=False
        is_b_found:bool=False
        with open("./SOLIS.cfg","r",encoding='utf-8') as file:
            for line in file:
                line=line.rstrip()
                if line=="APP_LOOPBACK_PORT":
                    lp_port_a="COM"+file.readline().rstrip()
                    is_a_found=True
                elif line=="APP_PORT":
                    lp_port_b="COM"+file.readline().rstrip()
                    is_b_found=True
        if is_a_found and is_b_found:
            return True, lp_port_a, lp_port_b
        else:
            return False, "", ""
    else:
        return True, lp_port_a,lp_port_b

if __name__=="__main__":
    print(get_com_ports())
    print(find_loop_back())
    print(find_stage())
    print(find_loop_back_or_default())
    print(find_stage_or_default())
