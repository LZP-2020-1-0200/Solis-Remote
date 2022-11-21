"""Module that loads, saves, and updates all session data"""
from typing import TypedDict
import datetime
import json



_dictionary={}
_dictionary["points"]=[]
_dictionary["experiments"]=[]
_dictionary["refs"]=[]

_dir=""

def set_session_directory(dir:str)->None:
    global _dir
    _dir=dir

def save():
    """saves the data to session.json"""
    global _dictionary
    with open(_dir+"/session.json", "w") as sessionFile:
        json.dump(_dictionary,sessionFile,indent=4)

def load():
    """loads the session.json from dictionary"""
    global _dictionary
    with open(_dir+"/session.json", "r") as sessionFile:
        _dictionary=json.load(sessionFile)
    
def get_data_points():
    """Gets datapoints from json"""
    global _dictionary

    return _dictionary["points"]

def get_pt_list():
    """Acquires the newest list of points in as a list of tuples of x and y coordinates"""
    return [(item["x"],item["y"]) for item in _dictionary["points"]]

def set_data_points(points:list[tuple[int,int]]):
    """Sets datapoints"""
    global _dictionary

    _dictionary["points"]=[]
    for ind,pt in enumerate(points):
        _dictionary["points"].append({"x":pt[0],"y":pt[1],"filename":f"{str(ind+1).zfill(5)}.asc"})

def add_experiment(folder:str,name:str)->None:
    """Add an experiment entry to the json file"""
    global _dictionary

    _dictionary["experiments"].append({"folder":folder,"name":name,"timestamp":str(datetime.datetime.now())})
    save()

def add_reference(filepath:str,type:str):
    """Add a reference entry to the json file"""
    global _dictionary

    _dictionary["refs"].append({"file":filepath,"type":type,"timestamp":str(datetime.datetime.now())})
    save()