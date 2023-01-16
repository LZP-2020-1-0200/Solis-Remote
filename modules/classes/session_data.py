"""Module that loads, saves, and updates all session data"""
import datetime
import json
import os
import logging
from tkinter import messagebox
from typing import Any

from .coordinate import Coordinate
from .event import CustomEvent
from ..helpers import translator
from .logger import Logger

log:logging.Logger=Logger(__name__).get_logger()

class SessionDataPoint():
    """A data struct of a single point"""
    def __init__(self,x_coordinate:int|float,y_coordinate:int|float,filename:str) -> None:
        self.coordinate:Coordinate=Coordinate(x_coordinate,y_coordinate)
        self.filename:str=filename
    def pack(self)->dict[str,Any]:
        """Packs the datapoint into a dictionary"""
        # round the datapoint coordinates before packing
        return {"x":round(self.coordinate.x),"y":round(self.coordinate.y),"filename":self.filename}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'SessionDataPoint':
        """returns a new instance of `sessionDataPoint` containing data from `dictionary`"""
        return SessionDataPoint(dictionary["x"],dictionary["y"],dictionary["filename"])

class SessionDataExperiment():
    """A data struct of an experiment"""
    def __init__(self,folder:str,name:str,timestamp:str) -> None:
        self.folder:str=folder
        self.name:str=name
        self.timestamp:str=timestamp
    def pack(self)->dict[str,Any]:
        """Packs the experiment object into a dictionary"""
        return {"folder":self.folder,"name":self.name,"timestamp":self.timestamp}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'SessionDataExperiment':
        """returns a new instance of `sessionDataExperiment` containing data from `dictionary`"""
        return SessionDataExperiment(
            dictionary["folder"],
            dictionary["name"],
            dictionary["timestamp"])

class SessionDataReference():
    """A data struct of a reference."""
    def __init__(self,file:str,reference_type:str,timestamp:str) -> None:
        self.file:str=file
        self.type:str=reference_type
        self.timestamp:str=timestamp

    def pack(self)->dict[str,Any]:
        """Packs the reference into a dictionary"""
        return {"file":self.file,"type":self.type,"timestamp":self.timestamp}

    @staticmethod
    def unpack(dictionary:dict[str,Any]) -> 'SessionDataReference':
        """returns a new instance of `sesstionDataReference` containing data from `dictionary`"""
        return SessionDataReference(dictionary["file"],dictionary["type"],dictionary["timestamp"])


class SessionData():
    """Acts as a struct with functionallity of packing and unpacking data
    from a dictionary (json) format
    """
    def __init__(self) -> None:
        self.points_set:bool=False
        self.anchors_set:bool=False
        self.local_anchors_set:bool=False
        self.points:list[SessionDataPoint]=[]
        self.experiments:list[SessionDataExperiment]=[]
        self.references:list[SessionDataReference]=[]
        self.anchors:list[Coordinate]=[]

        self.local_points:list[SessionDataPoint]=[]
        self.local_anchors:list[Coordinate]=[]
        self.dir:str=""

        self.last_anchors:list[Coordinate]=[]

        self.onstatuschange:CustomEvent=CustomEvent("session_data.onstatuschange")
        self.onpointchange:CustomEvent=CustomEvent("session_data.onpointchange")

    def pack(self)->dict[str,Any]:
        """Creates a dictionary from the values"""
        return {
            "flags":{
                "points_set":self.points_set,
                "anchors_set":self.anchors_set
                },
            "points":[point.pack() for point in self.points],
            "refs":[reference.pack() for reference in self.references],
            "anchors":[anchor.to_dict(rounding=True) for anchor in self.anchors],
            "experiments":[exp.pack() for exp in self.experiments],
            "last_anchors":[anchor.to_dict(rounding=True) for anchor in self.last_anchors]
            }
    def unpack(self, dictionary:dict[str, Any]) -> bool:
        """Extracts values from a dictionary."""
        no_problems_found:bool=True
        if "flags" in dictionary:
            if "points_set" in dictionary["flags"]:
                self.points_set=dictionary["flags"]["points_set"]
            else:
                log.warning("Points set flag not found.")
                no_problems_found=False

            if "anchors_set" in dictionary["flags"]:
                self.anchors_set=dictionary["flags"]["anchors_set"]
            else:
                log.warning("Anchors set flag not found.")
                no_problems_found=False
        else:
            log.warning("Flags not found in dictionary.")
            no_problems_found=False

        if "points" in dictionary:
            self.points=[SessionDataPoint.unpack(point) for point in dictionary["points"]]
        else:
            log.warning("Points not found in dictionary.")
            no_problems_found=False

        if "experiments" in dictionary:
            self.experiments=[
                SessionDataExperiment.unpack(experiment)
                for experiment in dictionary["experiments"]
                ]
        else:
            log.warning("Experiments not found in dictionary.")
            no_problems_found=False

        if "refs" in dictionary:
            self.references=[
                SessionDataReference.unpack(reference)
                for reference in dictionary["refs"]
            ]
        else:
            log.warning("References not found in dictionary.")
            no_problems_found=False

        if "anchors" in dictionary:
            self.anchors=[Coordinate.from_dict(coord) for coord in dictionary["anchors"]]
        else:
            log.warning("Anchors not found in dictionary.")
            no_problems_found=False

        self.local_points=[]

        if "last_anchors" in dictionary:
            self.last_anchors=[Coordinate.from_dict(coord) for coord in dictionary["last_anchors"]]
        else:
            log.warning("Last anchors not found in dictionary.")
            no_problems_found=False
        if not no_problems_found:
            messagebox.showwarning(#type: ignore
                title="Problems loading session",
                message="The json file is lacking one or more of the necessary files. "+
                "Please add the missing fields in the json file and try again. "+
                "See logs for missing fields.")
            return False


        # Local points is set if, and only if the point setting process was halted half way,
        #   that is, points were set, but the anchors were not
        if self.points_set and not self.anchors_set:
            log.warning("Points were set, but anchors were not in the unpacked session")
            messagebox.showwarning( #type: ignore
                title="Problems opening session",
                message="This session has points set, however, no anchors were set.\n"+
                        "If the sample has been moved, please create a new session.")
            # make a deep copy
            self.local_points=[
                SessionDataPoint(pt.coordinate.x,pt.coordinate.y,pt.filename)
                for pt in self.points
                ]
        return True

data_struct:SessionData=SessionData()


# --- Save/Load ---
def save() -> None:
    """saves the data to session.json"""
    log.info("Saving data")
    with open(data_struct.dir+"/session.json", "w", encoding="utf-8") as session_file:
        json.dump(data_struct.pack(),session_file,indent=4)

def load() -> bool:
    """loads the session.json from dictionary"""
    log.info("Loading data")
    with open(data_struct.dir+"/session.json", "r", encoding="utf-8") as session_file:
        if not data_struct.unpack(json.load(session_file)):
            return False
    data_struct.onstatuschange()
    data_struct.onpointchange()
    return True

def calculate_relative_points() -> None:
    """Calculates local points from anchors and stored points"""
    log.info("Translating stored points to local coordinates")
    local_coords: list[Coordinate]=[
        translator.anchor_translate(data_struct.local_anchors,data_struct.anchors,item.coordinate)
        for item in data_struct.points
        ]
    # make a copy with translated coordinates
    data_struct.local_points=[
        SessionDataPoint(local_coords[ind].x,local_coords[ind].y,item.filename)
        for ind,item in enumerate(data_struct.points)
        ]

# --- Getters ---
def get_pt_list() -> list[tuple[int | float, int | float]]:
    """Acquires the newest list of points in as a list of tuples of x and y coordinates"""
    return [item.coordinate.to_tuple() for item in data_struct.local_points]

# --- Setters ---
def set_local_anchors(anchor_a:Coordinate, anchor_b:Coordinate, anchor_c:Coordinate) -> None:
    """Sets the local anchors and global anchors if none are set"""
    log.info("Setting local anchors")
    #set local anchors and the flag
    data_struct.local_anchors=[anchor_a,anchor_b,anchor_c]
    data_struct.local_anchors_set=True
    #set last anchors
    data_struct.last_anchors=[anchor_a,anchor_b,anchor_c]
    #set global anchors if none are set
    if not data_struct.anchors_set:
        _set_anchors()
    calculate_relative_points()
    data_struct.onstatuschange()

def _set_anchors() -> None:
    """Sets the session's anchors to the local anchors (used only on first initialization)"""
    log.info("Setting global anchors")
    data_struct.anchors=[Coordinate(anchor.x,anchor.y) for anchor in data_struct.local_anchors]
    data_struct.anchors_set=True
    save()
    data_struct.onstatuschange()

def load_last_anchors() -> bool:
    """If anchors were ever set, load last known anchors"""
    if data_struct.anchors_set:
        try:
            assert len(data_struct.last_anchors)==3
            set_local_anchors(
                data_struct.last_anchors[0],
                data_struct.last_anchors[1],
                data_struct.last_anchors[2])
            messagebox.showinfo("Loading Successful", "Last known anchors set.")#type: ignore
            return True
        except AssertionError:
            log.error("The anchor flag was set, but last_anchors were not.", exc_info=True)
    messagebox.showerror("Unable to load last anchors.", "No anchors have been set.")#type: ignore
    return False

def add_data_point(point:Coordinate) -> None:
    """Adds a point to the local point list"""
    log.info("Single datapoint added")
    data_struct.local_points.append(SessionDataPoint(
        point.x,
        point.y,
        str(len(data_struct.local_points)+1).zfill(5)+".asc"
        ))
    data_struct.onpointchange()
def add_data_points(points:list[Coordinate]) -> None:
    """Adds a list of points to the local point list"""
    log.info("Multiple datapoints added")
    for point in points:
        data_struct.local_points.append(SessionDataPoint(
            point.x,
            point.y,
            str(len(data_struct.local_points)+1).zfill(5)+".asc"
            ))
    data_struct.onpointchange()
def pop_data_point() -> None:
    """Removes last datapoint from the local point list"""
    log.info("Removed last datapoint")
    data_struct.local_points.pop()
    data_struct.onpointchange()
def clear_data_points() -> None:
    """Clears all datapoints from the local point list"""
    log.info("Cleared all datapoints")
    data_struct.local_points=[]
    data_struct.onpointchange()

def submit_data_points() -> None:
    """Copies all locally set points to the json file"""
    log.info("Saving all datapoints")
    data_struct.points_set=True
    #deep copy
    data_struct.points=[
        SessionDataPoint(pt.coordinate.x,pt.coordinate.y,pt.filename)
        for pt in data_struct.local_points
        ]
    save()
    data_struct.onpointchange()
    data_struct.onstatuschange()

def add_experiment(folder:str,name:str)->None:
    """Add an experiment entry to the json file"""
    log.info("Appending an experiment entry")
    data_struct.experiments.append(SessionDataExperiment(
        folder,
        name,
        timestamp=str(datetime.datetime.now())
        ))
    save()

def add_reference(filepath:str,ref_type:str) -> None:
    """Add a reference entry to the json file"""
    log.info("Appending reference entry")
    data_struct.references.append(SessionDataReference(
        file=filepath,
        reference_type=ref_type,
        timestamp=str(datetime.datetime.now())
        ))
    save()

# --- First setup ---

def session_setup() -> None:
    """creates the initial setup for a session"""
    log.info("Making directories")
    os.mkdir(data_struct.dir+"/experiments/")
    os.mkdir(data_struct.dir+"/refs/")
    save()
