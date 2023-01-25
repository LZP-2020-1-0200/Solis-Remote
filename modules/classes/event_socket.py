"""Contains a class containing a singleton for broadcasting events"""
import socket
import threading
from enum import IntEnum

PORT_NUMBER:int=56123


class SockEventType(IntEnum):
    """A basic enum that really is only meant
    for sending a CAPTURE signal to the gx capture pc
    """
    SET_DIR = 1
    CAPTURE = 2

class EventSocket():
    """A singleton that creates TCP connections and sends events"""
    __instance:'EventSocket | None'=None
    __generated:bool=False
    def __new__(cls) -> 'EventSocket':
        if EventSocket.__instance is None:
            EventSocket.__instance=object.__new__(cls)
        return EventSocket.__instance


    def __init__(self) -> None:
        if not EventSocket.__generated:
            self.__socket: socket.socket=socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM)
            self.__socket.settimeout(1)
            self.__socket.bind(('',PORT_NUMBER))
            self.__socket.listen(5)
            self.__out_sockets:list[socket.socket]=[]
            self.__accept_cons:bool=True
            # create a seperate thread that accepts all incoming connections.
            # this thread get's killed on program exit
            self.__acceptor:threading.Thread=threading.Thread(target=self.__accept,daemon=True)
            self.__acceptor.start()
            EventSocket.__generated=True

    def __del__(self) -> None:
        self.__accept_cons=False
        self.__acceptor.join()

    def __accept(self) -> None:
        while self.__accept_cons:
            incoming_socket:socket.socket
            try:
                incoming_socket, _ = self.__socket.accept()
                self.__out_sockets.append(incoming_socket)
            except socket.timeout:
                pass

    def broadcast(self, message:bytes) -> None:
        """Sends bytes to all connections,
        removes connection from list if message fails to deliver
        """
        removables:list[socket.socket]=[]
        for sock in self.__out_sockets:
            rem:int=len(message)
            head_failed:bool=False
            try:
                while rem!=0:
                    #print(message[-rem:])
                    b_sent:int=sock.send(message[-rem:])
                    #print(rem, b_sent)
                    if b_sent==0:
                        head_failed=True
                        break
                    rem-=b_sent
            except socket.error:
                head_failed=True

            if head_failed:
                removables.append(sock)
                continue
        for remov in removables:
            self.__out_sockets.remove(remov)

    def send_event(self, event:SockEventType) -> None:
        """Broadcasts an event to all connections"""
        self.broadcast(event.to_bytes(length=1, byteorder='big'))

if __name__=="__main__":
    server_sock:EventSocket=EventSocket()
    print("server created")
    while 1:
        input()
        server_sock.send_event(SockEventType.CAPTURE)
