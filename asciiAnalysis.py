#pylint: disable=all
#type: ignore

import os.path
import os
import json
from tkinter import filedialog
import re
import matplotlib.pyplot as plt
from typing import Any
import numpy as np
from numpy.typing import NDArray
from numpy import polynomial

def get_cmap(n:int, name:str='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def parseAsciiFile(rawtext:str) -> tuple[NDArray[np.float64], NDArray[Any], dict[Any, Any]]:
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



dir:str=""
while True:
    dir = filedialog.askdirectory(title="Select Session directory")
    if os.path.isfile(os.path.join(dir,"session.json")):
        break
# JSON file
f: Any = open (os.path.join(dir,"session.json"), "r")
data:dict[str,Any] = json.load(f)
print(data["refs"])
f.close()

analysisDir: str=os.path.join(dir,"analysis")
if not os.path.isdir(analysisDir):
    os.mkdir(analysisDir)

plotDir: str=os.path.join(dir,"analysis/plots")
if not os.path.isdir(plotDir):
    os.mkdir(plotDir)
mapDir: str=os.path.join(dir,"analysis/colorMaps")
if not os.path.isdir(mapDir):
    os.mkdir(mapDir)
peakDir: str=os.path.join(dir,"analysis/peaks")
if not os.path.isdir(peakDir):
    os.mkdir(peakDir)


fig, (plt1,plt2) = plt.subplots(1,2)
fig.set_size_inches(12,6)

refsReq: list[str]=["dark","white","darkForWhite"]

darkX:NDArray[np.float64]=np.array([])
darkY:NDArray[np.float64]=np.array([])
whiteX:NDArray[np.float64]=np.array([])
whiteY:NDArray[np.float64]=np.array([])
d4wX:NDArray[np.float64]=np.array([])
d4wY:NDArray[np.float64]=np.array([])

for ref in reversed(data["refs"]):
    if ref["type"]==refsReq[0]:
        with open(os.path.join(dir,ref["file"])) as f:
            darkX,darkY,_=parseAsciiFile(f.read())
        break

for ref in reversed(data["refs"]):
    if ref["type"]==refsReq[1]:
        with open(os.path.join(dir,ref["file"])) as f:
            whiteX,whiteY,_=parseAsciiFile(f.read())
        break

for ref in reversed(data["refs"]):
    if ref["type"]==refsReq[2]:
        with open(os.path.join(dir,ref["file"])) as f:
            d4wX,d4wY,_=parseAsciiFile(f.read())
        break



clrmp=get_cmap(len(data["experiments"])+1)

#readIn[dataPoint][experiment][1 (intensityData)][valueAtWavelength]
#readIn[dataPoint][experiment][0 (waveData)][Wavelength]
readIn:list[list[Any]]=[]
maxV:None|float=None
minV:float=0

# data parsing and early transformations
for ind, point in enumerate(data["points"][20:380]):
    readIn.append([])
    for expInd, exp in enumerate(data["experiments"]):
        ptDir: str=os.path.join(dir,exp["folder"],point["filename"])
        f=open(ptDir,mode="r")
        pX,pY,pH=parseAsciiFile(f.read())
        f.close()
        displayY: NDArray[np.float64]=np.divide((pY-darkY),(whiteY-d4wY))
        readIn[ind].append((pX,displayY,pH))
        m:float=np.max(displayY)
        if maxV is None or m>maxV:
            maxV=m
if maxV is None: maxV=0
maxV*=1.1
lk: dict[str, float]={"Water": 1.333, "EtOH": 1.363, "Air":1.0, "PBS":1.335}

experimentMaxMovement:list[list[list[Any]]]=[]
for i in range(len(data["experiments"])):
    experimentMaxMovement.append([[],[]])

# Function approximation and critical point acquisition
for ind, point in enumerate(data["points"][20:380]):
    #clear plot data and re-set the y-axis limits
    plt1.cla()
    plt2.cla()
    
    plt2.set_ylim([np.min(d4wX),np.max(d4wX)])
    plt1.set_ylim([minV,maxV])
    for expInd,exp in enumerate(data["experiments"]):

        # polynomial approximation
        pX,displayY,pH=readIn[ind][expInd]
        fit=polynomial.Polynomial.fit(pX,displayY,15)

        # maximum point filtering by use of derivative

        # all critical points
        fitD=fit.deriv(1)
        criticals=fitD.roots()
        fit2ndD=fit.deriv(2)
        #fit3rdD=fit.deriv(3)
        # filter complex roots
        arr = np.real(criticals[np.isreal(criticals)])

        #filter out of range roots
        arr=arr[arr < np.max(pX)]
        arr=arr[arr>np.min(pX)] 

        #filter minimum points
        minimums=arr[fit2ndD(arr)>0]

        arr=arr[fit2ndD(arr) < 0]
        
        
        # amplitude filter
        
        #horizontal bounds of a maximum (the value for which you are sure will be less than the difference between peaks) 
        peakWidth=25
        #the difference (in % of the total amplitude) of the bounds that could be considered a peak
        peakRelativeAmplitude=0.005
        arr=arr[fit(arr)-fit(np.clip(arr+peakWidth,np.min(pX),np.max(pX)))>maxV*peakRelativeAmplitude]
        arr=arr[fit(arr)-fit(np.clip(arr-peakWidth,np.min(pX),np.max(pX)))>maxV*peakRelativeAmplitude]

        nearbyThreshold=30
        for peak in arr:
            added=False
            uniqueMaxPoints=experimentMaxMovement[expInd][0]
            uniqueMaximums=experimentMaxMovement[expInd][1]
            for uniqueI, uniqueMax in enumerate(uniqueMaximums):
                if abs(peak-uniqueMax[-1])<nearbyThreshold and abs(fit(peak)-fit(uniqueMax[-1]))<0.2 and ind-uniqueMaxPoints[uniqueI][-1]<=2:
                    uniqueMax.append(peak)
                    uniqueMaxPoints[uniqueI].append(ind)
                    added=True
                    break
            if not added:
                uniqueMaximums.append([peak])
                uniqueMaxPoints.append([ind])
            


        #plotting
        plt1.plot(pX,fit(pX),label=exp["name"]+"_"+os.path.basename(exp["folder"]),color=clrmp(expInd))
        plt1.scatter(pX,displayY,s=0.01,color=clrmp(expInd))
        plt1.scatter(arr,fit(arr),s=15,color=clrmp(expInd))
        plt1.legend()
        if exp["name"] in lk.keys():
            plt2.scatter(np.full_like(arr,lk[exp["name"]]) ,arr,color=clrmp(expInd),s=15,label=exp["name"]+"_"+os.path.basename(exp["folder"]))
        else:
            print("Refractive index for "+exp["name"]+" is not found")
        #plt2.plot(pX,fit(pX),label=exp["name"]+"_"+os.path.basename(exp["folder"]))
        #plt2.legend()
    #saving the results and displaying them on a screen for a short moment
    plt.savefig(os.path.join(plotDir,f"{str(ind).zfill(6)}.png"))
    #plt.draw()
    #plt.pause(0.2)

plt.draw()
plt.cla()
plt.clf()

for eI,experiment in enumerate(experimentMaxMovement):
    uniqueMaxPoints=experiment[0]
    uniqueMaximums=experiment[1]
    plt.cla()
    plt.clf()
    
    plt.xlim(0,100)
    plt.ylim(np.min(darkX),np.max(darkX))
    for ind,um in enumerate(uniqueMaximums):
        plt.scatter(np.array(uniqueMaxPoints[ind]),np.array(um))
    plt.savefig(os.path.join(peakDir,data["experiments"][eI]["name"]+"_"+str(eI)+".png"))

    #plt.show()
plt.cla()
plt.clf()
plt.xlabel("Wavelength λ (nm)")
plt.ylabel("x-position")


#swap the axes for ease of access
axisSwap = np.swapaxes(readIn,0,2)
#point values for all points in experiments
experimentIntensities=axisSwap[1]
for expId in range(len(data["experiments"])):
    # reformat from array of arrays to a 2d array
    intensities=experimentIntensities[expId]
    colormap=np.stack(intensities)
    colormap=np.flip(colormap,0)

    plt.imshow(colormap,cmap="plasma",aspect='auto',extent=[np.min(d4wX),np.max(d4wX),0,len(colormap)])
    plt.savefig(os.path.join(mapDir,str(os.path.basename(data["experiments"][expId]["folder"]))+"_"+str(data["experiments"][expId]["name"])+".png"))
