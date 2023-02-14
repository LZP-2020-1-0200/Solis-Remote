"""Contains a class containing a singleton for broadcasting events"""
import socket
import threading
from enum import IntEnum

PORT_NUMBER:int=56123
TCP_V2=True

class SockEventType(IntEnum):
    """A basic enum that really is only meant
    for sending a CAPTURE signal to the gx capture pc
    Further entries to the enum can be added for additional devices and events
    """
    CAPTURE = 2
    EXPERIMENT_ID = 0

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
            self.__stop_accepting:threading.Event=threading.Event()
            # create a seperate thread that accepts all incoming connections.
            # this thread get's killed on program exit
            self.__acceptor:threading.Thread=threading.Thread(target=self.__accept)
            self.__acceptor.start()
            EventSocket.__generated=True

    def __del__(self) -> None:
        self.__stop_accepting.set()
        self.__acceptor.join()
        EventSocket.__instance=None

    def __accept(self) -> None:
        while not self.__stop_accepting.is_set():
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
        msg_size: int = len(message)
        # toggleable message length prefix while in transition phase
        full_msg: bytes = msg_size.to_bytes(4,'big') if TCP_V2 else b''
        full_msg=full_msg+message
        removables:list[socket.socket]=[]
        for sock in self.__out_sockets:
            rem:int=len(full_msg)
            head_failed:bool=False
            try:
                while rem!=0:
                    b_sent:int=sock.send(full_msg[-rem:])
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

    def ask_capture(self, point_id:int):
        """sends a broadcast that orders a capture"""
        self.broadcast(
            SockEventType.CAPTURE.to_bytes(length=1,byteorder='big')+
            point_id.to_bytes(length=4, byteorder='big'))

    # TODO: integrate experiments into capture
    def set_experiment(self, experiment_id:int):
        """sends a broadcast that signals a change in experiment"""
        self.broadcast(
            SockEventType.EXPERIMENT_ID.to_bytes(length=1,byteorder='big')+
            experiment_id.to_bytes(length=2,byteorder='big'))


if __name__=="__main__":
    server_sock:EventSocket=EventSocket()
    print("server created")
    try:
        while 1:
            i = input()
            if len(i)==0:
                server_sock.send_event(SockEventType.CAPTURE)
            elif i.isnumeric():
                server_sock.set_experiment(int(i))
            else:
                server_sock.broadcast(b'random_msg testing')
    finally:
        del server_sock
