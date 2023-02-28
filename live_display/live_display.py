import socket
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import numpy as np
from numpy.typing import NDArray
import base64
import json
import glob
import threading
import os
import shutil
import PIL.Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ASCIIPoint:
    def __init__(self, path:str) -> None:
        f=open(path,mode="r")
        self.x,self.y,self.headers = self._parseFile(f.read())
        f.close()
    
    def _parseFile(self,rawtext:str):
        text: str= rawtext.replace(",",".")
        headerParams: list[str]=re.findall(".+:.+(?=\r?\n)",text)
        headerData: dict[str, str]={x[0]:x[1].lstrip() for x in [item.split(":",1) for item in headerParams]}
        
        split: list[str]=re.findall("[0-9.]+\t[0-9.]+\r?\n",text)
        tSplit: list[list[str]]=[item.rstrip().split("\t") for item in split]
        x: NDArray[np.float64]=np.array([float(item[0]) for item in tSplit])
        time:str=""
        if "Exposure Time (secs)" in headerData.keys():
            time=headerData["Exposure Time (secs)"]
        else:
            time=headerData["Accumulate Cycle Time (secs)"]

        accs:int=1
        if "Number of Accumulations" in headerData.keys():
            accs=int(headerData["Number of Accumulations"])
        y: NDArray[np.float64]=(np.array([int(item[1]) for item in tSplit])/accs)/float(time)
        return (x,y,headerData)

ascii_dir=""
img_dir=""
stay_alive=True
    



def parse_message(message):
    lines = message.split("\r\n")
    topic = base64.b64decode(lines[0])
    
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
receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def drawer():
    global ascii_dir, img_dir
    while stay_alive:
        try:
            receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            receiver.connect(("192.168.5.19",28325))
            topics=["experiment"]
            receiver.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            receiver.sendall(b"\r\n".join([base64.b64encode(t.encode()) for t in topics])+b"\0")
            receiver.settimeout(0.1)
            databuf=b""
            while stay_alive:
                data=b""
                try:
                    data = receiver.recv(2048)
                    if len(data)==0:
                        break
                except socket.timeout:
                    continue
                databuf=databuf+data
                ind = databuf.find(b'\0\r\n')
                if ind!=-1:
                    message=parse_message(databuf[:ind].decode())["data"]
                    ascii_dir="P:\\"+message["dir"]
                    img_dir="P:\\"+message["img_dir"]
                    databuf=databuf[ind+3:]
        except socket.error:
            pass

threading.Thread(target=drawer).start()
plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(12,6)
last_ascii=""
try:
    while plt.get_fignums():
        if ascii_dir!="" and img_dir!="":
            asciis=sorted(glob.glob(ascii_dir+"\\*"), key=os.path.getctime, reverse=True)
            if len(asciis)>0:
                ascii_path=asciis[0]
                if last_ascii!=ascii_path:
                    last_ascii=ascii_path
                    os.path.basename(ascii_path)
                    img_path=os.path.join(img_dir, os.path.basename(ascii_path)+".jpg")
                    ax1.clear()
                    ax2.clear()
                    ax2.set_axis_off()
                    pt = ASCIIPoint(ascii_path)
                    fig.suptitle(os.path.basename(ascii_path))
                    ax1.plot(pt.x, pt.y)
                    if os.path.exists(img_path):
                        img=PIL.Image.open(img_path)
                        img.thumbnail((400,400))
                        ax2.imshow(img)
                    os.makedirs(os.path.join(img_dir, "figs"), exist_ok=True)
                    plt.savefig(os.path.join(img_dir, "figs",os.path.basename(ascii_path)+".jpg"))
            plt.draw()
            plt.gcf().canvas.draw_idle()
            plt.gcf().canvas.start_event_loop(0.6)
    
finally:
    stay_alive=False
    receiver.close()

