
import serial #type: ignore
import serial.tools.list_ports #type: ignore

def get_com_ports() -> list[str]:
    return [item.name for item in list(serial.tools.list_ports.comports())]#type:ignore

def find_loop_back() -> tuple[bool,str,str]:
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

if __name__=="__main__":
    print(get_com_ports())
    print(find_loop_back())
    print(find_stage())