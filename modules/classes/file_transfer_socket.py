"""Implements a socket for receiving files (pictures in particular)
and saving them to specific sessions and experiments
"""

import socket
import os
import threading
if __name__!="__main__":
    from .session_data import data_struct
def _get_experiment_folder(exp_ind:int) -> str:
    """fetches the specific experiment's relative directory
    returns custom directory if file launched by itself
    """
    if __name__=="__main__":
        return "exp"+str(exp_ind)
    else:
        return data_struct.experiments[exp_ind].folder

def _get_session_dir() -> str:
    """fetches the session directory
    (redirects to local directory if file launched by itself)
    """
    if __name__=="__main__":
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),"..","..","test")
    else:
        return data_struct.dir

def _get_point_filename(num:int) -> str:
    """fetches the filename of a specific point
    returns custom name if file launched by itself
    """
    if __name__=="__main__":
        return str(num).zfill(5)
    else:
        return data_struct.points[num].filename


PORT_NUMBER:int=56124
class FTSocket():
    """A singleton that listens for TCP connections and saves files"""
    __instance:'FTSocket | None'=None
    __generated:bool=False
    def __new__(cls) -> 'FTSocket':
        if FTSocket.__instance is None:
            FTSocket.__instance=object.__new__(cls)
        return FTSocket.__instance


    def __init__(self) -> None:
        if not FTSocket.__generated:
            self.__socket: socket.socket=socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM)
            self.__socket.settimeout(30)
            self.__socket.bind(('',PORT_NUMBER))
            self.__socket.listen(5)
            self.__stop_accepting:threading.Event=threading.Event()
            # create a seperate thread that accepts all incoming connections.
            # this thread get's killed on program exit
            self.__acceptor:threading.Thread=threading.Thread(target=self.__accept,daemon=True)
            self.__acceptor.start()
            FTSocket.__generated=True

    def __del__(self) -> None:
        self.__stop_accepting.set()
        self.__acceptor.join()

    def __save_file(self, sock:socket.socket) -> bool:
        """Saves a file, returns True if file was received"""
        # read message header
        # file_length   exp_id     img_type     img_num
        # (4 bytes)     (2 byte)   (1 byte)     (4_bytes)

        # check if sock is sending a new header
        first_bytes: bytes = sock.recv(4)
        if first_bytes==b'':
            return False
        file_length: int=int.from_bytes(first_bytes, 'big')
        experiment_id:int=int.from_bytes(sock.recv(2), 'big')
        img_type:int = int.from_bytes(sock.recv(1), 'big')
        img_num: int=int.from_bytes(sock.recv(4), 'big')

        # if img type is not 0, 1, or 2 assume a random binary file
        img_ext:str=".bin"
        if img_type==0:
            img_ext=".jpg"
        elif img_type==1:
            img_ext=".tif"
        elif img_type==2:
            img_ext=".png"

        img_path: str=os.path.join( _get_session_dir(),'imgs',_get_experiment_folder(experiment_id))
        os.makedirs(img_path,exist_ok=True)
        full_path:str=os.path.join(img_path,_get_point_filename(img_num)+img_ext)
        bytes_remaining:int=file_length
        print(file_length)
        with open(full_path,'wb') as image_file:
            while bytes_remaining>0:
                print(file_length, "/", file_length-bytes_remaining)
                read_b=sock.recv(min(bytes_remaining,4096))
                if len(read_b)==0:
                    return False
                image_file.write(read_b)
                bytes_remaining-=len(read_b)
        return True

    def __accept(self) -> None:
        while not self.__stop_accepting.is_set():
            incoming_socket:socket.socket
            try:
                incoming_socket, _ = self.__socket.accept()
                # save a file (one file per connection)
                self.__save_file(incoming_socket)
                incoming_socket.shutdown(socket.SHUT_RDWR)
                incoming_socket.close()
            except socket.timeout:
                pass
            except socket.error:
                pass


if __name__=="__main__":
    FTSocket()
    #sock:socket.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #sock.connect(("127.0.0.1",PORT_NUMBER))
    #test_bytes=b'Testing\n123dsa sa\r\n'
    #message:bytes= len(test_bytes).to_bytes(4,'big')+
    # (0).to_bytes(1,'big')+
    # (3).to_bytes(1,'big')+
    # (0).to_bytes(4,'big')+
    # test_bytes
    #sock.sendall(message)
    input()
    #sock.shutdown(socket.SHUT_RDWR)
    #sock.close()
