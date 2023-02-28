import socket
import base64
import json
import time
import threading
import shutil
import glob
from pathlib2 import Path
import os



def parse_message(topics, message):
    lines = message.split("\r\n")
    topic = base64.b64decode(lines[0])
    if topic not in topics:
        return False
    
    # parse all parameters
    params={}
    for line in lines[1:]:
        if line == '':
            break
        data=line.split(":")
        params[data[0].strip()]=data[1].strip()
    
    # parse it if it's a string
    if params["type"]=="string":
        o = {"topic": topic, "data":base64.b64decode(lines[-1])}
        o.update(params)
        return o
    # or a json file
    elif params["type"]=="json":
        o={"topic": topic, "data":json.loads(lines[-1])}
        o.update(params)
        return o
    # any other type is passed in raw
    else:
        o={"topic": topic, "data":lines[-1]}
        o.update(params)
        return o


def get_subscribed_message(topics):
    while True:
        try:
            receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            receiver.connect(("192.168.5.19",28325))
            print("connected")
            receiver.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            ts=[]
            for t in topics:
                ts.append(base64.b64encode(t))
            receiver.sendall("\r\n".join(ts)+"\0")
            print("topics established.")
            receiver.settimeout(0.1)
            databuf=""
            while True:
                data=""
                try:
                    data = receiver.recv(2048)
                    if len(data)==0:
                        break
                except socket.timeout:
                    yield False
                    continue
                databuf=databuf+data
                ind = databuf.find('\0\r\n')
                if ind!=-1:

                    
                    yield parse_message(topics, databuf[:ind])
                    databuf=databuf[ind+3:]
        except socket.error:
            print("\nconnection error..")
            yield False


import pyautogui
def take_capture():
    time.sleep(1.2)
    pyautogui.moveTo(10, 10, duration = 0.1)
    buttonbox=pyautogui.locateOnScreen('.\\button.PNG',grayscale=True,minSearchTime=2,region=(0,0,500,500))
    print(buttonbox)
    if buttonbox is not None:
        pyautogui.click(pyautogui.center(buttonbox))
        #sleep so the button becomes grayed out
        pyautogui.moveTo(10, 10, duration = 0.1)
        time.sleep(2)
        # wait until the button is available to be pressed
        while pyautogui.locateOnScreen('.\\button.PNG', minSearchTime=2, region=(0,0,500,500)) is None:
            time.sleep(0.1)
            print("where button?")
        print("button found again")
        return True
    else:
        print("Button not found. Taking screenshot instead")
        return quick_capture()
        
def quick_capture():
    time.sleep(0.66)
    cam_region=(221, 50, 766, 570)
    pyautogui.screenshot('.\\imgs\\'+str(time.time())+".jpg",region=cam_region)
    return True

mode_lock=threading.Lock()
use_fast=False
should_quit=False

def mode_switch():
    global use_fast, mode_lock, should_quit
    while True:
        print("currently using "+("fast" if use_fast else "slow")+" capturing")
        inp=raw_input()
        with mode_lock:
            use_fast=not use_fast

def get_glob(ft):
    return glob.glob('.\\imgs\\*'+ft)


def file_sender(t_name, t_dir):
        img_glob = get_glob(".jpg")+get_glob(".tif")+get_glob(".png")
        gl = sorted(img_glob, key=os.path.getctime, reverse=True)
        while len(gl)==0:
            time.sleep(0.1)
            gl = sorted(img_glob, key=os.path.getctime, reverse=True)
        file_name = gl[0]
        if file_name!="":
            buffer_folder='.\\backup\\'
            new_name=os.path.join(buffer_folder, os.path.basename(file_name))
            ext=os.path.splitext(new_name)[1]
            try:
                shutil.move(file_name,buffer_folder)
                shutil.copy(new_name, os.path.join("P:\\", t_dir, t_name+ext))
            except WindowsError:
                print("file not available yet, waiting for free file")
                os.remove(new_name)
                time.sleep(0.2)


if __name__=="__main__":
    mode_switch_thread = threading.Thread(target=mode_switch)
    mode_switch_thread.start()
    try:
        msg = get_subscribed_message(["capture"])
        cont=True
        while cont:
            rec_msg = next(msg)
            if rec_msg==False:
                with mode_lock:
                    if should_quit:
                        cont=False
            elif rec_msg==None:
                break
            elif rec_msg["topic"]=="capture":
                capture_data=rec_msg["data"]
                with mode_lock:
                    was_successful=False
                    if use_fast:
                        was_successful = quick_capture()
                    else:
                        was_successful = take_capture()
                    if was_successful:
                        Path(os.path.join("P:\\",capture_data["dir"])).mkdir(exist_ok=True, parents=True)
                        file_sender(capture_data["picture_name"], capture_data["dir"])
    except KeyboardInterrupt:
        pass
    mode_switch_thread.join()
