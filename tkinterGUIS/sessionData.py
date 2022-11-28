"""Module that loads, saves, and updates all session data"""
from typing import TypedDict
from classes.coordinate import Coordinate
from helpers.gaussianElimination import gaussianElimination2D
import datetime
import json
import numpy as np



_dictionary={}
_dictionary["points"]=[]
_dictionary["experiments"]=[]
_dictionary["refs"]=[]
_dictionary["anchors"]=[]

_anchors=[]
_local_points=[]

_dir=""


def anchor_translate(originalAnchors:list[dict],originalPoint:dict)->Coordinate:
    """Returns a translated point to local anchors"""
    #generate coords from anchors
    a:Coordinate=Coordinate(originalAnchors[0]["x"],originalAnchors[0]["y"])
    b:Coordinate=Coordinate(originalAnchors[1]["x"],originalAnchors[1]["y"])
    c:Coordinate=Coordinate(originalAnchors[2]["x"],originalAnchors[2]["y"])

    #core vectors
    ab=b-a
    ac=c-a

    ogCoord:Coordinate=Coordinate(originalPoint["x"],originalPoint["y"])

    # get relative coordinate to a
    relOgCoord=ogCoord-a

    aug=np.array([
        [ab.x,ac.x,relOgCoord.x],
        [ab.y,ac.y,relOgCoord.y]
    ])
    solved=gaussianElimination2D(aug)
    


    #compositional scalars
    #comp1:float=relOgCoord.asComponentOf(ab)
    #comp2:float=relOgCoord.asComponentOf(ac)

    #core vectors of this session
    abL=_anchors[1]-_anchors[0]
    acL=_anchors[2]-_anchors[0]

    #core vectors multiplied by their scalars create the absolute coordinate
    return _anchors[0] + abL*solved[0]+acL*solved[1]







def set_local_anchors(a:Coordinate,b:Coordinate,c:Coordinate):
    global _anchors
    _anchors=[a,b,c]

def set_anchors():
    global _local_points
    _dictionary["anchors"]=[{"x":item.x,"y":item.y} for item in _anchors]

    local_coords=[anchor_translate(_dictionary["anchors"],item) for item in _dictionary["points"]]
    _local_points=[{"x":item.x,"y":item.y,"filename":_dictionary["points"][ind]["filename"]} for ind,item in enumerate(local_coords)]

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
    global _dictionary, _local_points
    with open(_dir+"/session.json", "r") as sessionFile:
        _dictionary=json.load(sessionFile)
    local_coords=[anchor_translate(_dictionary["anchors"],item) for item in _dictionary["points"]]
    _local_points=[{"x":item.x,"y":item.y,"filename":_dictionary["points"][ind]["filename"]} for ind,item in enumerate(local_coords)]

    
def get_data_points():
    """Gets datapoints from json"""
    global _local_points
    return _local_points

def get_pt_list():
    """Acquires the newest list of points in as a list of tuples of x and y coordinates"""
    global _local_points
    return [(item["x"],item["y"]) for item in _local_points]

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