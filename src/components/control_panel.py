from tkinter import Frame, StringVar, Button, Label, Entry, LEFT, X, filedialog, Checkbutton, BooleanVar
from model.data_parser import MapData
from model.constances import EMPTY_NUMBER
from .distance_func_frame import DistanceFuncFrame
from event.event_dispatcher import evtDispatcher
from event.event_ids import EvtIds
import os

class ControlPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.numBtns = []
        self.selectedNum = EMPTY_NUMBER
        self.numberPanel = Frame(self)
        self.create_number_buttons(self.numberPanel)

        self.settingPanel = None
        self.strRow = StringVar()
        self.strCol = StringVar()
        self.picPath = ""
        self.okBtn = None
        self.create_setting_panel()

        self.funcPanel = None
        self.btnLoadImg = None
        self.btnClearAll = None
        self.btnSave = None
        self.create_func_panel()
        self.row = 0
        self.col = 0

        self.distancePanel = DistanceFuncFrame(self)

        self.numberPanel.pack(expand=1)
        self.settingPanel.pack(expand=1)
        self.funcPanel.pack(expand=1)
        self.distancePanel.pack(expand=1)
        self.deactive_buttons()

        evtDispatcher.register(EvtIds.EVT_PROJECT_CREATED, self.handle_active_control_panel)
        evtDispatcher.register(EvtIds.EVT_PROJECT_LOADED, self.handle_active_control_panel)

    def handle_active_control_panel(self, content):
        self.active_buttons()

    def deactive_buttons(self):
        for numBtn in self.numBtns:
            numBtn['state'] = 'disabled'
        self.btnClearAll['state'] = 'disabled'
        self.btnLoadImg['state'] = 'disabled'
        self.btnSave['state'] = 'disabled'
        self.okBtn['state'] = 'disabled'

    def active_buttons(self):
        for numBtn in self.numBtns:
            numBtn['state'] = 'normal'
        self.btnClearAll['state'] = 'normal'
        self.btnLoadImg['state'] = 'normal'
        self.btnSave['state'] = 'normal'
        self.okBtn['state'] = 'normal'

    def create_number_buttons(self, parent):
        w = 10
        self.numBtns.append(Button(parent, width=w, text = "0", command = lambda : self.on_number_button_clicked(0)))
        self.numBtns.append(Button(parent, width=w, text = "1", command = lambda : self.on_number_button_clicked(1)))
        self.numBtns.append(Button(parent, width=w, text = "2", command = lambda : self.on_number_button_clicked(2)))
        self.numBtns.append(Button(parent, width=w, text = "3", command = lambda : self.on_number_button_clicked(3)))
        self.numBtns.append(Button(parent, width=w, text = "4", command = lambda : self.on_number_button_clicked(4)))
        self.numBtns.append(Button(parent, width=w, text = "5", command = lambda : self.on_number_button_clicked(5)))
        self.numBtns.append(Button(parent, width=w, text = "6", command = lambda : self.on_number_button_clicked(6)))
        self.numBtns.append(Button(parent, width=w, text = "7", command = lambda : self.on_number_button_clicked(7)))
        self.numBtns.append(Button(parent, width=w, text = "8", command = lambda : self.on_number_button_clicked(8)))
        self.numBtns.append(Button(parent, width=w, text = "9", command = lambda : self.on_number_button_clicked(9)))
        self.numBtns.append(Button(parent, width=w, text = "*", command = lambda : self.on_number_button_clicked(10)))
        self.numBtns.append(Button(parent, width=w, text = "#", command = lambda : self.on_number_button_clicked(11)))
        row = 0
        col = 0
        for btn in self.numBtns:
            btn.grid(row=row, column=col, sticky="NSEW")
            if col == 3:
                col = 0
                row = row + 1
            else:
                col = col + 1

    def create_setting_panel(self):
        inputWidth = 10
        self.settingPanel = Frame(self)
        lbl1 = Label(self.settingPanel, text="row")
        input1 = Entry(self.settingPanel, textvariable=self.strRow, width=inputWidth)
        lbl2 = Label(self.settingPanel, text="   col")
        input2 = Entry(self.settingPanel, textvariable=self.strCol, width=inputWidth)
        lblEmpty = Label(self.settingPanel, text="   ")
        self.okBtn = Button(self.settingPanel, text="OK", command=self.on_ok_button_clicked, bd=5)
        lbl1.pack(fill=X, side=LEFT, expand=1)
        input1.pack(fill=X, side=LEFT, expand=1)
        lbl2.pack(fill=X, side=LEFT, expand=1)
        input2.pack(fill=X, side=LEFT, expand=1)
        lblEmpty.pack(fill=X, side=LEFT, expand=1)
        self.okBtn.pack(fill=X, side=LEFT, expand=1)
        self.strRow.set("50")
        self.strCol.set("50")

    def create_func_panel(self):
        self.funcPanel = Frame(self)
        btnWidth = 20
        self.btnLoadImg = Button(self.funcPanel, text="load image", width=btnWidth, bd=4, command=self.on_load_image_clicked)
        self.btnClearAll = Button(self.funcPanel, text="clear all", width=btnWidth, bd=4, command=self.on_clear_all_clicked)
        self.btnSave = Button(self.funcPanel, text="save", width=btnWidth, bd=4, command=self.on_save_button_clicked)
        self.btnLoadImg.pack(expand=1)
        self.btnClearAll.pack(expand=1)
        self.btnSave.pack(expand=1)

    def on_number_button_clicked(self, num):
        self.selectedNum = num
        for btn in self.numBtns:
            btn['state'] = "normal"
        self.numBtns[num]['state'] = "disabled"
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_NUMBER_CHANGED, {"number": self.selectedNum})

    def on_ok_button_clicked(self):
        try:
            row = int(self.strRow.get())
            col = int(self.strCol.get())
            if row > 0 and col > 0:
                self.row = row
                self.col = col
                evtDispatcher.dispatch(EvtIds.EVT_INFORM_TO_DRAW_GRIDS, {"row": self.row, "col": self.col})
        except Exception as e:
            print(str(e))

    def on_load_image_clicked(self):
        filename = filedialog.askopenfilename(initialdir = ".", title = "Select a picture", filetypes = (("png files","*.png"), ("all files","*.*")))
        if filename and len(filename) > 0:
            evtDispatcher.dispatch(EvtIds.EVT_INFORM_LOAD_PICTURE, {"imgpath": filename})

    def on_clear_all_clicked(self):
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_CLEAR_NUMBERS, None)
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_CLEAR_PATH, None)

    def on_save_button_clicked(self):
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_SAVE_PROJECT, {"filepath": self.parent.projectPath})
