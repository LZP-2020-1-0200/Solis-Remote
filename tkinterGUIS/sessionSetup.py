from tkinter import * 
from tkinter import messagebox
import json
import os

def sessionSetup(dir,points):
    if messagebox.askyesno("","Have all points been recorded?"):
        os.mkdir(dir+"/experiments/")
        os.mkdir(dir+"/refs/")
        json_file={}
        json_file["points"]=[]
        json_file["experiments"]=[]
        i=1
        for pt in points:
            json_file["points"].append({"x":pt[0],"y":pt[1],"filename":f"{str(i).zfill(5)}.asc"})
            i+=1
        with open(dir+"/session.json", "w") as outfile:
            outfile.write(json.dumps(json_file, indent=4))
        return json_file


