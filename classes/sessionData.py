"""Module that loads, saves, and updates all session data"""
import datetime
import json
import os
from tkinter import messagebox
from typing import Any

from classes.coordinate import Coordinate
from classes.event import CustomEvent
from helpers import translator
from classes.logger import Logger
import logging

log:logging.Logger=Logger(__name__).get_logger()


class sessionDataPoint():
    def __init__(self,x:int|float,y:int|float,filename:str) -> None:
        self.coordinate:Coordinate=Coordinate(x,y)
        self.filename:str=filename
    def pack(self)->dict[str,Any]:
        """Packs the datapoint into a dictionary"""

        # round the datapoint coordinates before packing
        return {"x":round(self.coordinate.x),"y":round(self.coordinate.y),"filename":self.filename}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'sessionDataPoint':
        """returns a new instance of `sessionDataPoint` containing data from `dictionary`"""
        return sessionDataPoint(dictionary["x"],dictionary["y"],dictionary["filename"])

class sessionDataExperiment():
    def __init__(self,folder:str,name:str,timestamp:str) -> None:
        self.folder:str=folder
        self.name:str=name
        self.timestamp:str=timestamp
    def pack(self)->dict[str,Any]:
        """Packs the experiment object into a dictionary"""
        return {"folder":self.folder,"name":self.name,"timestamp":self.timestamp}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'sessionDataExperiment':
        """returns a new instance of `sessionDataExperiment` containing data from `dictionary`"""
        return sessionDataExperiment(dictionary["folder"],dictionary["name"],dictionary["timestamp"])

    

class sessionDataReference():
    def __init__(self,file:str,type:str,timestamp:str) -> None:
        self.file:str=file
        self.type:str=type
        self.timestamp:str=timestamp
    def pack(self)->dict[str,Any]:
        """Packs the reference into a dictionary"""
        return {"file":self.file,"type":self.type,"timestamp":self.timestamp}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'sessionDataReference':
        """returns a new instance of `sesstionDataReference` containing data from `dictionary`"""
        return sessionDataReference(dictionary["file"],dictionary["type"],dictionary["timestamp"])


class sessionData():
    """Acts as a struct with functionallity of packing and unpacking data from a dictionary (json) format"""
    def __init__(self) -> None:
        self.points_set:bool=False
        self.anchors_set:bool=False
        self.local_anchors_set:bool=False
        self.points:list[sessionDataPoint]=[]
        self.experiments:list[sessionDataExperiment]=[]
        self.references:list[sessionDataReference]=[]
        self.anchors:list[Coordinate]=[]

        self.local_points:list[sessionDataPoint]=[]
        self.local_anchors:list[Coordinate]=[]
        self.dir:str=""

    def pack(self)->dict[str,Any]:
        return {
            "flags":{
                "points_set":self.points_set,
                "anchors_set":self.anchors_set
                },
            "points":[point.pack() for point in self.points],
            "refs":[reference.pack() for reference in self.references],
            "anchors":[anchor.toDict(rounding=True) for anchor in self.anchors],
            "experiments":[exp.pack() for exp in self.experiments]
            }
    def unpack(self, dictionary:dict[str, Any]) -> None:
        self.points_set=dictionary["flags"]["points_set"]
        self.anchors_set=dictionary["flags"]["anchors_set"]
        self.points=[sessionDataPoint.unpack(point) for point in dictionary["points"]]
        self.experiments=[sessionDataExperiment.unpack(experiment) for experiment in dictionary["experiments"]]
        self.references=[sessionDataReference.unpack(reference) for reference in dictionary["refs"]]
        self.anchors=[Coordinate(coord["x"],coord["y"]) for coord in dictionary["anchors"]]
        self.local_points=[]
        
        # Local points is set if, and only if the point setting process was halted half way, 
        #   that is, points were set, but the anchors were not
        if self.points_set and not self.anchors_set:
            log.warning("Points were set, but anchors were not in the unpacked session")
            messagebox.showwarning( # type: ignore  - surpresses a warning that is caused by showwarning()
                title="Problems opening session",
                message="This session has points set, however, no anchors were set.\nIf the sample has been moved, please create a new session.")
            # make a deep copy
            self.local_points=[sessionDataPoint(pt.coordinate.x,pt.coordinate.y,pt.filename) for pt in self.points]
            

dataStruct:sessionData=sessionData()


onstatuschange:CustomEvent=CustomEvent()
onstatuschange.bind(lambda:log.info("onstatuschange called"))
onpointchange:CustomEvent=CustomEvent()
onpointchange.bind(lambda:log.info("onpointchange called"))


# --- Save/Load ---

def save() -> None:
    """saves the data to session.json"""
    log.info("Saving data")
    with open(dataStruct.dir+"/session.json", "w") as sessionFile:
        json.dump(dataStruct.pack(),sessionFile,indent=4)

def load() -> None:
    """loads the session.json from dictionary"""
    log.info("Loading data")
    with open(dataStruct.dir+"/session.json", "r") as sessionFile:
        dataStruct.unpack(json.load(sessionFile))
    onstatuschange()
    onpointchange()

def calculateRelativePoints() -> None:
    log.info("Translating stored points to local coordinates")
    local_coords: list[Coordinate]=[translator.anchor_translate(dataStruct.local_anchors,dataStruct.anchors,item.coordinate) for item in dataStruct.points]
    # make a copy with translated coordinates
    dataStruct.local_points=[sessionDataPoint(local_coords[ind].x,local_coords[ind].y,item.filename) for ind,item in enumerate(dataStruct.points)]


# --- Getters ---

def get_pt_list() -> list[tuple[int | float, int | float]]:
    """Acquires the newest list of points in as a list of tuples of x and y coordinates"""
    return [item.coordinate.toTuple() for item in dataStruct.local_points]


# --- Setters ---
#def set_status(flag:str,value:bool):
    #_dictionary["flags"][flag]=value
    #save()
    #onstatuschange()


def set_local_anchors(a:Coordinate,b:Coordinate,c:Coordinate) -> None:
    log.info("Setting local anchors")
    dataStruct.local_anchors=[a,b,c]
    #_local_markers_set=True
    dataStruct.local_anchors_set=True
    if not dataStruct.anchors_set:
        _set_anchors()
    calculateRelativePoints()
    onstatuschange()

def _set_anchors() -> None:
    """Sets the session's anchors to the local anchors (used only on first initialization)"""
    log.info("Setting global anchors")
    #_dictionary["anchors"]=[{"x":item.x,"y":item.y} for item in _anchors]
    dataStruct.anchors=[Coordinate(anchor.x,anchor.y) for anchor in dataStruct.local_anchors]
    #_dictionary["flags"]["anchors_set"]=True
    dataStruct.anchors_set=True
    save()
    onstatuschange()

def add_data_point(point:Coordinate) -> None:
    """Adds a point to the local point list"""
    log.info("Single datapoint added")
    #_local_points.append({"x":round(point.x),"y":round(point.y),"filename":str(len(_local_points)+1).zfill(5)+".asc"})
    dataStruct.local_points.append(sessionDataPoint(point.x,point.y, str(len(dataStruct.local_points)+1).zfill(5)+".asc"))
    onpointchange()
def add_data_points(points:list[Coordinate]) -> None:
    """Adds a list of points to the local point list"""
    log.info("Multiple datapoints added")
    for point in points:
        dataStruct.local_points.append(sessionDataPoint(point.x,point.y, str(len(dataStruct.local_points)+1).zfill(5)+".asc"))
    onpointchange()
def pop_data_point() -> None:
    log.info("Removed last datapoint")
    dataStruct.local_points.pop()
    onpointchange()
def clear_data_points() -> None:
    log.info("Cleared all datapoints")
    dataStruct.local_points=[]
    onpointchange()

def submit_data_points() -> None:
    """Copies all locally set points to the json file"""
    log.info("Saving all datapoints")
    dataStruct.points_set=True
    #deep copy
    dataStruct.points=[sessionDataPoint(pt.coordinate.x,pt.coordinate.y,pt.filename) for pt in dataStruct.local_points]
    save()
    onpointchange()
    onstatuschange()

def add_experiment(folder:str,name:str)->None:
    """Add an experiment entry to the json file"""
    log.info("Appending an experiment entry")
    dataStruct.experiments.append(sessionDataExperiment(folder,name,timestamp=str(datetime.datetime.now())))
    save()

def add_reference(filepath:str,type:str) -> None:
    """Add a reference entry to the json file"""
    log.info("Appending reference entry")
    dataStruct.references.append(sessionDataReference(file=filepath,type=type,timestamp=str(datetime.datetime.now())))
    save()


# --- First setup ---

def sessionSetup() -> None:
    """creates the initial setup for a session"""
    log.info("Making directories")
    os.mkdir(dataStruct.dir+"/experiments/")
    os.mkdir(dataStruct.dir+"/refs/")
    save()

