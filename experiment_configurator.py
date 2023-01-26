"""Adds additional info to sessions for easier data analysis"""
if __name__ =="__main__":
    from typing import TypeAlias, Literal, Union, LiteralString
    from modules.classes import session_data
    from tkinter import filedialog, simpledialog, messagebox
    import os
    import shutil

    RefType:TypeAlias = Union[Literal["white"], Literal["dark"], Literal["darkForWhite"]]

    session_dir:str = filedialog.askdirectory(title="Select session directory")
    if session_dir=="":
        quit()
    with open(os.path.join(session_dir,"session.json"), encoding="utf-8") as f:
        session_data.data_struct.dir=session_dir
        session_data.load()

    def list_experiments() -> str:
        """Lists all experiments"""
        out:str=""
        for ind, ex in enumerate(session_data.data_struct.experiments):
            out+=str(ind+1)+" "+str(ex.timestamp)+" "+str(ex.name)+"\n"
        return out

    def list_type_references(ref_type:RefType) -> str:
        """Lists all references of a specific type, retaining original indices"""
        out:str=""
        for ind, ref in enumerate(session_data.data_struct.references):
            if ref.type==ref_type:
                out+=str(ind+1)+" "+str(ref.timestamp)+" "+str(ref.file)+"\n"
        return out

    def prompt_ref(ref_type:RefType) -> int:
        """Prompts user to select a reference"""
        while 1:
            li:str=list_type_references(ref_type)
            __resp: int | None=simpledialog.askinteger(title="",prompt=li+"Select reference: ")
            if isinstance(__resp,int):
                ref_ind:int=__resp-1
                if session_data.data_struct.references[ref_ind].type==ref_type:
                    return ref_ind
            else:
                messagebox.showinfo(message="Bad input")
        return 0



    ex_ind:int=0
    while 1:
        li:str=list_experiments()
        exPrompt:int|None=simpledialog.askinteger(title="",
            prompt=li+"Select which experiment to configure: ")
        if isinstance(exPrompt, int):
            ex_ind=int(exPrompt)-1
            break

    current_exp:session_data.SessionDataExperiment=session_data.data_struct.experiments[ex_ind]

    def image_setting() -> None:
        """Moves images to a session-relative directory, renames them to corresponding point"""
        os.makedirs(os.path.join(session_dir,"imgs",current_exp.folder),exist_ok=True)
        img_dir:str = filedialog.askdirectory(title="Select image directory")
        if img_dir!="":
            list_of_files: list[str] = sorted(
                filter( lambda x: os.path.isfile(os.path.join(img_dir, x)),
                os.listdir(img_dir) ) )
            img_destination_path: str=os.path.join(session_dir,"imgs",current_exp.folder)
            for fname, point in zip(list_of_files, session_data.data_struct.points):
                point_basename:str='.'.join(point.filename.split('.')[:-1])
                img_ext:str=fname.split('.')[-1]
                img_filename: str=point_basename + '.' + img_ext
                shutil.copy2(
                    os.path.join(img_dir, fname),
                    os.path.join(img_destination_path, img_filename))
            current_exp.img_dir=os.path.relpath(path=img_destination_path,start=session_dir)

    while 1:
        choice:int=0
        while 1:
            PROMPT: LiteralString=("1: set white ref\n"+
            "2: set dark ref\n"+
            "3: set d4w ref\n"+
            "4: set images\n"+
            "5: change experiment\n"+
            "6: quit\n")
            resp:int|None = simpledialog.askinteger(title="",prompt=PROMPT+"Choose your action: ")
            if isinstance(resp, int):
                choice=resp
                break
            #resp:str=input("Choose your action: ")
            #if resp.isnumeric():
            #    choice=int(resp)
            #    break
        if choice==6:
            break
        if choice==1:
            current_exp.white_index=prompt_ref(ref_type='white')
        elif choice==2:
            current_exp.dark_index=prompt_ref(ref_type="dark")
        elif choice==3:
            current_exp.d4w_index=prompt_ref(ref_type='darkForWhite')
        elif choice==4:
            image_setting()
        elif choice==5:
            while 1:
                li=list_experiments()
                exPrompt=simpledialog.askinteger(title="",
                    prompt=li+"Select which experiment to configure: ")
                if isinstance(exPrompt, int):
                    ex_ind=int(exPrompt)-1
                    break
            current_exp=session_data.data_struct.experiments[ex_ind]
        else:
            messagebox.showinfo(message="Bad input")
        session_data.save()
else:
    raise ImportError(name="File is not a module")
