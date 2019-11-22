import os
from copy import deepcopy
from tkinter import Menu, filedialog, Frame, StringVar, LEFT, Button, Entry, Toplevel, messagebox, Label
from model.constances import PROJECT_SUFFIX
from model.data_parser import DataParser
from event.event_dispatcher import evtDispatcher
from event.event_ids import EvtIds

class FileSubmenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent, tearoff=0, bd=5)
        self.newProjectPanel = None
        self.projPath = StringVar()
        self.add_command(label="新建工程", command=self.new_project)
        self.add_command(label="打开工程", command=self.open_project)

    def open_project(self):
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select project", filetypes = (("mg files","*.mg"), ))
        mapdata = DataParser().parse_from_file(filename)
        if mapdata is None:
            messagebox.showerror("error", "open project error!")
            return
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_GET_MAP_DATA, {"mapdata": deepcopy(mapdata)})
        evtDispatcher.dispatch(EvtIds.EVT_GET_PROJECT_NAME, {"path": filename})
        evtDispatcher.dispatch(EvtIds.EVT_PROJECT_LOADED, None)
    
    def new_project(self):
        self.newProjectPanel = Toplevel(self, bd=8)
        self.newProjectPanel.resizable(False, False)
        self.newProjectPanel.wm_attributes("-topmost", True)
        self.newProjectPanel.title("Create project")
        inputPanel = Frame(self.newProjectPanel)
        ctrlPanel = Frame(self.newProjectPanel)
        Entry(inputPanel, textvariable=self.projPath, bd=4, width=60).pack(side=LEFT)
        Button(inputPanel, text="Open Dir", command=self.open_dir).pack(side=LEFT)
        Button(ctrlPanel, text="Confirm", command=self.create_project_ok).pack(side=LEFT)
        Label(ctrlPanel, text="               ").pack(side=LEFT)
        Button(ctrlPanel, text="Cancel", command=self.close_new_project_panel).pack(side=LEFT)
        inputPanel.pack()
        Label(self.newProjectPanel, text="").pack()
        ctrlPanel.pack()
        self.newProjectPanel.update()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        ww = self.newProjectPanel.winfo_width()
        wh = self.newProjectPanel.winfo_height()
        self.newProjectPanel.geometry("+%d+%d" % (int((sw-ww)/2), int((sh-wh)/2)))
    
    def open_dir(self):
        dirpath = filedialog.askdirectory(title="Set save directory", initialdir=".", mustexist=True, parent=self.newProjectPanel)
        projectName = "NewProject"
        filepath = os.path.join(dirpath, projectName + PROJECT_SUFFIX)
        counter = 1
        while os.path.exists(filepath):
            projectName = "NewProject(%d)" % counter
            filepath = os.path.join(dirpath, projectName + PROJECT_SUFFIX)
            counter += 1
        if dirpath:
            self.projPath.set("%s/%s" % (dirpath, projectName))
    
    def close_new_project_panel(self):
        self.newProjectPanel.destroy()
        self.newProjectPanel = None
    
    def create_project_ok(self):
        filepath = self.projPath.get() + PROJECT_SUFFIX
        if os.path.exists(filepath):
            messagebox.showerror("Error", "project exists")
        else:
            open(filepath, "wb").close()
        self.close_new_project_panel()
        evtDispatcher.dispatch(EvtIds.EVT_GET_PROJECT_NAME, {"path": filepath})
        evtDispatcher.dispatch(EvtIds.EVT_PROJECT_CREATED, None)