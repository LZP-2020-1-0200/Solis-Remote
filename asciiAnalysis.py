import os.path
import json
from tkinter import filedialog
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from matplotlib import cm
from numpy import polynomial


def parseAsciiFile(text:str):
    headerParams=re.findall(".+:.+(?=\r?\n)",text)
    headerData={x[0]:x[1].lstrip() for x in [item.split(":",1) for item in headerParams]}
    text=text.replace(",",".")
    split=re.findall("[0-9.]+\t[0-9.]+\r?\n",text)
    tSplit=[item.rstrip().split("\t") for item in split]
    x=np.array([float(item[0]) for item in tSplit])
    y=(np.array([int(item[1]) for item in tSplit])/int(headerData["Number of Accumulations"]))/float(headerData["Accumulate Cycle Time (secs)"])
    return (x,y,headerData)



dir=None
while True:
    dir = filedialog.askdirectory(title="Select Session directory")
    if os.path.isfile(os.path.join(dir,"session.json")):
        break
# JSON file
f = open (os.path.join(dir,"session.json"), "r")
data = json.load(f)
print(data["experiments"])
f.close()

fig, (plt1,plt2) = plt.subplots(1,2)

f=filedialog.askopenfile(mode="r",title="Select dark reference",defaultextension=".asc",initialdir=os.path.join(dir,"refs"))
darkX,darkY,darkH=parseAsciiFile(f.read())
f.close()
#plt2.plot(darkX,darkY)

f=filedialog.askopenfile(mode="r",title="Select white reference",defaultextension=".asc",initialdir=os.path.join(dir,"refs"))
whiteX,whiteY,whiteH=parseAsciiFile(f.read())
f.close()
#plt3.plot(whiteX,whiteY)

f=filedialog.askopenfile(mode="r",title="Select dark for white reference",defaultextension=".asc",initialdir=os.path.join(dir,"refs"))
d4wX,d4wY,d4wH=parseAsciiFile(f.read())
f.close()
#plt4.plot(d4wX,d4wY)



for point in data["points"]:
    plt1.cla()
    plt2.cla()
    for exp in data["experiments"]:
        ptDir=os.path.join(dir,exp["folder"],point["filename"])
        f=open(ptDir,mode="r")
        pX,pY,pH=parseAsciiFile(f.read())
        f.close()
        displayY=np.divide((pY-darkY),(whiteY-d4wY))
        fit=polynomial.Polynomial.fit(pX,displayY,15)
        criticals=fit.deriv().roots()
        fit2ndD=fit.deriv(2)
        
        arr = criticals[np.isreal(criticals) ]

        arr=arr[arr < np.max(pX)]
        arr=arr[arr>np.min(pX)] 
        arr=arr[fit2ndD(arr)<0]



        print(arr)
        plt1.plot(pX,fit(pX))
        plt1.scatter(pX,displayY,label=exp["name"],s=1)
        plt2.scatter(arr,fit(arr),s=15)
        plt2.plot(pX,fit(pX))
    plt.draw()
    plt.pause(0.2)




#plt.plot(whiteX,whiteY)
plt.show()