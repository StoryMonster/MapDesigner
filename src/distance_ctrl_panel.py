from tkinter import Checkbutton, Label, Frame, BooleanVar
from constances import UNREACH_DISTANCE

class DistanceCtrlPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.isCalcDistanceMode = BooleanVar()
        self.cbCalcDistance = Checkbutton(self, variable=self.isCalcDistanceMode, text="calculate distance mode", command=self.on_calc_distance_cb_clicked)
        self.cbCalcDistance.deselect()
        self.lblStartPos = Label(self)
        self.lblEndPos = Label(self)
        self.lblDistance = Label(self)

        Label(self).pack(expand=1)
        Label(self).pack(expand=1)
        self.cbCalcDistance.pack(expand=1)
        self.lblStartPos.pack(expand=1)
        self.lblEndPos.pack(expand=1)
        self.lblDistance.pack(expand=1)
    
    def on_calc_distance_cb_clicked(self):
        if not self.is_calc_distance_mode():
            self.clean()

    def is_calc_distance_mode(self):
        return self.isCalcDistanceMode.get()

    def show_start_position(self, x, y):
        self.lblEndPos.config(text="")
        self.lblDistance.config(text="")
        self.lblStartPos.config(text="POS1: (%d, %d)" % (x, y))

    def show_end_position(self, x, y):
        self.lblEndPos.config(text="POS2: (%d, %d)" % (x, y))
        self.lblDistance.config(text="calculating...")

    def show_distance(self, val):
        if val == UNREACH_DISTANCE:
            self.lblDistance.config(text="UNREACHABLE")
            return
        self.lblDistance.config(text="Shortest Distance: %d" % val)

    def clean(self):
        self.lblStartPos.config(text="")
        self.lblEndPos.config(text="")
        self.lblDistance.config(text="")
        self.parent.clear_path_grids()

