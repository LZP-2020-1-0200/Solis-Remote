"""Adds additional info to sessions for easier data analysis"""
if __name__ =="__main__":
    from typing import TypeAlias, Literal, Union
    from modules.classes import session_data
    from tkinter import filedialog, simpledialog
    import os
    import shutil

    RefType:TypeAlias = Union[Literal["white"], Literal["dark"], Literal["darkForWhite"]]

    session_dir:str = filedialog.askdirectory(title="Select session directory")
    if session_dir=="":
        quit()
    with open(os.path.join(session_dir,"session.json"), encoding="utf-8") as f:
        session_data.data_struct.dir=session_dir
        session_data.load()

    def list_experiments() -> None:
        """Lists all experiments"""
        for ind, ex in enumerate(session_data.data_struct.experiments):
            print(ind+1, ex.timestamp, ex.name)

    def list_type_references(ref_type:RefType) -> None:
        """Lists all references of a specific type, retaining original indices"""
        for ind, ref in enumerate(session_data.data_struct.references):
            if ref.type==ref_type:
                print(ind+1, ref.timestamp, ref.file)

    def prompt_ref(ref_type:RefType) -> int:
        """Prompts user to select a reference"""
        while 1:
            list_type_references(ref_type)
            __resp: int | None=simpledialog.askinteger(title="",prompt="Select reference: ")
            if isinstance(__resp,int):
                ref_ind:int=__resp
                if session_data.data_struct.references[ref_ind].type==ref_type:
                    return ref_ind
        return 0



    ex_ind:int=0
    while 1:
        list_experiments()
        exPrompt:int|None=simpledialog.askinteger(title="",
            prompt="Select which experiment to configure: ")
        if isinstance(exPrompt, int):
            ex_ind=int(exPrompt)-1
            break

    selected_experiment: session_data.SessionDataExperiment=session_data.data_struct.experiments[ex_ind]

    def image_setting() -> None:
        os.makedirs(os.path.join(session_dir,"imgs",selected_experiment.folder),exist_ok=True)
        img_dir:str = filedialog.askdirectory()
        if img_dir!="":
            list_of_files: list[str] = sorted(
                filter( lambda x: os.path.isfile(os.path.join(img_dir, x)),
                os.listdir(img_dir) ) )
            img_destination_path: str=os.path.join(session_dir,"imgs",selected_experiment.folder)
            for fname, point in zip(list_of_files, session_data.data_struct.points):
                shutil.move(
                    os.path.join(img_dir,fname),
                    os.path.join(img_destination_path,point.filename+"."+fname.split(".")[-1]))

    while 1:
        choice:int=0
        while 1:
            PROMPT=("1: set white ref\n"+
            "2: set dark ref\n"+
            "3: set d4w ref\n"+
            "4: set images\n"+
            "5: change experiment\n"+
            "6: quit\n")
            resp: int | None = simpledialog.askinteger(title="",prompt=PROMPT+"Choose your action: ")
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
            selected_experiment.white_index=prompt_ref('white')
        elif choice==2:
            selected_experiment.dark_index=prompt_ref(ref_type="white")
        elif choice==3:
            selected_experiment.d4w_index=prompt_ref('darkForWhite')
        elif choice==4:
            image_setting()
        elif choice==5:
            n_session_dir:str = filedialog.askdirectory(title="Select session directory")
            if n_session_dir!="":
                with open(os.path.join(n_session_dir,"session.json"), encoding="utf-8") as f:
                    session_data.data_struct.dir=n_session_dir
                    session_data.load()
        session_data.save()
else:
    raise ImportError(name="File is not a module")
