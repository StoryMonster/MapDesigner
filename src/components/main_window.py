from tkinter import Tk, messagebox
from .control_panel import ControlPanel
from .display_panel import DisplayCanvas
from .menu import MainMenu
from model.data_parser import MapData, DataParser
from event.event_dispatcher import evtDispatcher
from event.event_ids import EvtIds

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.appName = "Map Designer"
        self.strTitle = self.appName
        self.title(self.strTitle)
        self.canvas = DisplayCanvas(self, 700, 700)
        self.canvas.grid(row=0, column=0)
        self.ctrlPanel = ControlPanel(self)
        self.ctrlPanel.grid(row=0, column=1)
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.config(menu=MainMenu(self))
        self.projectPath = ""
        self.dataParser = DataParser()
        evtDispatcher.register(EvtIds.EVT_GET_PROJECT_NAME, self.handle_get_project_info)
        evtDispatcher.register(EvtIds.EVT_CONTENT_CHANGED, self.handle_project_content_changed)
        self.put_windows_at_center()
    
    def put_windows_at_center(self):
        self.update()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        ww = self.winfo_width()
        wh = self.winfo_height()
        self.geometry("+%d+%d" % (int((sw-ww)/2), int((sh-wh)/2)))

    def handle_get_project_info(self, content):
        if content is None or content["path"] is None: return
        self.projectPath = content["path"]
        self.strTitle = self.appName + ' - ' + self.projectPath
        self.title(self.strTitle)

    def handle_project_content_changed(self, content):
        if content is None or content["isChanged"] is None: return
        if content["isChanged"]:
            self.strTitle = self.appName + ' - ' + self.projectPath + "*"
        else:
            self.strTitle = self.appName + ' - ' + self.projectPath
        self.title(self.strTitle)
