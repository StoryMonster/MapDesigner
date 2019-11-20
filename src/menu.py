import os
from tkinter import Menu, filedialog, Frame, StringVar, LEFT, Button, Entry, Toplevel, messagebox, Label
from constances import PROJECT_SUFFIX

class MainMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.filemenu = None
        self.newProjectPanel = None
        self.projPath = StringVar()
        self.create_file_menu()
    
    def create_file_menu(self):
        self.filemenu = Menu(self, tearoff=0, bd=5)
        self.filemenu.add_command(label="新建工程", command=self.new_project)
        self.filemenu.add_command(label="打开工程", command=self.open_project)
        self.add_cascade(label="文件", menu=self.filemenu)
    
    def open_project(self):
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select project", filetypes = (("mg files","*.mg"), ))
        self.parent.read_project(filename)
    
    def new_project(self):
        self.newProjectPanel = Toplevel(self, bd=8)
        self.newProjectPanel.resizable(False, False)
        self.newProjectPanel.title("Create project")
        inputPanel = Frame(self.newProjectPanel)
        ctrlPanel = Frame(self.newProjectPanel)
        Entry(inputPanel, textvariable=self.projPath, bd=4, width=60).pack(side=LEFT)
        Button(inputPanel, text="Open Dir", command=self.open_dir).pack(side=LEFT)
        Button(ctrlPanel, text="Confirm", command=self.create_project_ok).pack(side=LEFT)
        Label(ctrlPanel, text="     ").pack(side=LEFT)
        Button(ctrlPanel, text="Cancel", command=self.close_new_project_panel).pack(side=LEFT)
        inputPanel.pack()
        Label(self.newProjectPanel, text="").pack()
        ctrlPanel.pack()
    
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
            self.parent.active_all_control_buttons()
    
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
        self.parent.set_project_path(filepath)
        self.parent.active_all_control_buttons()