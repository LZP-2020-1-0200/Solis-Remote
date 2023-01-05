#type: ignore
import re
from numpy.typing import NDArray
import numpy as np
from numpy import polynomial



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
    
    def cancelOutReference(self, white:NDArray[np.float64], dark:NDArray[np.float64], dark4white:NDArray[np.float64]):
        deltaWhite:NDArray[np.float64]=white-dark4white
        self.y=np.divide((self.y-dark),deltaWhite)

    def peakFinder(self) -> None:
        # polynomial approximation
        #pX,displayY,pH=readIn[ind][expInd]
        fit=polynomial.Polynomial.fit(self.x,self.y,15)
        # maximum point filtering by use of derivative
        # all critical points
        fitD=fit.deriv(1)
        criticals=fitD.roots()
        fit2ndD=fit.deriv(2)
        #fit3rdD=fit.deriv(3)
        # filter complex roots
        arr = np.real(criticals[np.isreal(criticals)])
        #filter out of range roots
        arr=arr[arr < np.max(self.x)]
        arr=arr[arr>np.min(self.x)] 
        #filter minimum points
        minimums=arr[fit2ndD(arr)>0]
        arr=arr[fit2ndD(arr) < 0]
        
        
        # amplitude filter
        
        #horizontal bounds of a maximum (the value for which you are sure will be less than the difference between peaks) 
        peakWidth=25
        #the difference (in % of the total amplitude) of the bounds that could be considered a peak
        peakRelativeAmplitude=0.005
        arr=arr[fit(arr)-fit(np.clip(arr+peakWidth,np.min(self.x),np.max(self.x)))>maxV*peakRelativeAmplitude]
        arr=arr[fit(arr)-fit(np.clip(arr-peakWidth,np.min(self.x),np.max(self.x)))>maxV*peakRelativeAmplitude]
        return arr
    def getPeakMovements(self):
        peaks=self.peakFinder()
        uniqueXs=[]
        uniqueYs=[]
        nearbyThreshold=30
        for peak in peaks:
            added=False
            for uniqueI, uniqueMax in zip(uniqueXs,uniqueYs):
                if abs(peak-uniqueMax[-1])<nearbyThreshold and abs(fit(peak)-fit(uniqueMax[-1]))<0.2 and ind-uniqueMaxPoints[uniqueI][-1]<=2:
                    uniqueMax.append(peak)
                    uniqueMaxPoints[uniqueI].append(ind)
                    added=True
                    break
            if not added:
                uniqueYs.append([peak])
                uniqueXs.append([ind])
        return (uniqueXs,uniqueYs)
        
