import socket
import threading
import base64
import json
import time
from typing import Any

stop_lock = threading.Lock()
stop_join = False

socket_lock = threading.Lock()
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
subscribers:list[socket.socket]=[]

def _encode_b64(string:str|bytes):
    if isinstance(string, str):
        return base64.b64encode(string.encode("utf-8"))
    return base64.b64encode(string)

#def _decode_b64(b64_bytes:bytes|str):
#    return base64.b64decode(b64_bytes)

def _join_loop():
    while True:
        with stop_lock:
            if stop_join:
                break
        with socket_lock:
            try:
                sock,_ = broadcast_socket.accept()
                sock.settimeout(30)
                subscribers.append(sock)
            except TimeoutError:
                pass
        time.sleep(0.01)
    broadcast_socket.close()


join_thread = threading.Thread(target=_join_loop)

def init():
    with socket_lock:
        broadcast_socket.settimeout(0.01)
        broadcast_socket.bind(("192.168.5.19",28325))
        broadcast_socket.listen(3)
    join_thread.start()


def publish_string(topic: str, message:str):
    with socket_lock:
        for sub_socket in subscribers:
            # topic
            sub_socket.sendall(_encode_b64(topic)+b"\r\n")
            # type
            sub_socket.sendall(b"type: string\r\n")
            # seperator
            sub_socket.sendall(b"\r\n")
            # message encoded in b64
            sub_socket.sendall(_encode_b64(message))
            # end of data
            sub_socket.sendall(b"\0\r\n")

def publish_json(topic:str, dictionary:dict[Any, Any]):
    with socket_lock:
        rem_queue:list[socket.socket]=[]
        for sub_socket in subscribers:
            try:
                # topic
                sub_socket.sendall(_encode_b64(topic)+b"\r\n")
                # type
                sub_socket.sendall(b"type: json\r\n")
                # seperator
                sub_socket.sendall(b"\r\n")
                # message encoded in b64
                sub_socket.sendall(json.dumps(dictionary).encode("utf-8"))
                # end of data
                sub_socket.sendall(b"\0\r\n")
            except socket.error:
                rem_queue.append(sub_socket)
        for sock in rem_queue:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            subscribers.remove(sock)


init()
if __name__=="__main__":
    try:
        img_num=1
        while True:
            x = input()
            if x=="q":
                break
            publish_json("capture", {"experiment_number":24, "picture_name":str(img_num).zfill(5)+".asc", "dir":"test\\experiment\\024", "point_number":34})
            img_num+=1
    finally:
        with stop_lock:
            stop_join=True
        join_thread.join()

