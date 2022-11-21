from tkinter import * 
from tkinter import messagebox
import json
import os

from typing import TypedDict
from tkinterGUIS import sessionData



def sessionSetup(dir,points):
    """creates the initial setup for a session"""

    if messagebox.askyesno("","Have all points been recorded?"):

        os.mkdir(dir+"/experiments/")
        os.mkdir(dir+"/refs/")
        '''
        json_file={}
        json_file["points"]=[]
        json_file["experiments"]=[]
        json_file["refs"]=[]
        i=1
        for pt in points:
            json_file.points.append({"x":pt[0],"y":pt[1],"filename":f"{str(i).zfill(5)}.asc"})
            i+=1
        with open(dir+"/session.json", "w") as outfile:
            outfile.write(json.dumps(json_file, indent=4))
        return json_file
        '''
        sessionData.set_session_directory(dir)
        sessionData.set_data_points(points)
        sessionData.save()


