from tkinter import Checkbutton, Label, Frame, BooleanVar
from model.constances import UNREACH_DISTANCE, INVALID_ROW, INVALID_COL
from event.event_dispatcher import evtDispatcher
from event.event_ids import EvtIds

class DistanceFuncFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.isCalcDistanceMode = BooleanVar()
        self.isCriticalShortest = BooleanVar()
        self.cbCalcDistance = Checkbutton(self, variable=self.isCalcDistanceMode, text="calculate distance mode", command=self.on_calc_distance_mode_clicked)
        self.cbCriticalShortest = Checkbutton(self, variable=self.isCriticalShortest, text="critical")
        self.cbCalcDistance.deselect()
        self.cbCriticalShortest.deselect()
        self.lblStartPos = Label(self)
        self.lblEndPos = Label(self)
        self.lblDistance = Label(self)
        self.firstPosRow = INVALID_ROW
        self.firstPosCol = INVALID_COL

        Label(self).pack(expand=1)
        Label(self).pack(expand=1)
        self.cbCalcDistance.pack(expand=1)
        self.cbCriticalShortest.pack(expand=1)
        self.lblStartPos.pack(expand=1)
        self.lblEndPos.pack(expand=1)
        self.lblDistance.pack(expand=1)
        
        evtDispatcher.register(EvtIds.EVT_FIRST_POSITION_SELECTED, self.handle_first_position_selected)
        evtDispatcher.register(EvtIds.EVT_SECOND_POSITION_SELECTED, self.handle_second_position_selected)
        evtDispatcher.register(EvtIds.EVT_SHORTEST_DISTANCE_CALCULATED, self.handle_shortest_distance_calculated)

    def handle_first_position_selected(self, content):
        if content is None or content["row"] is None or content["col"] is None: return
        self.lblEndPos.config(text="")
        self.lblDistance.config(text="")
        self.lblStartPos.config(text="POS1: (%d, %d)" % (content["col"], content["row"]))
        self.firstPosRow = content["row"]
        self.firstPosCol = content["col"]

    def handle_second_position_selected(self, content):
        if content is None or content["row"] is None or content["col"] is None: return
        self.lblEndPos.config(text="POS2: (%d, %d)" % (content["col"], content["row"]))
        self.lblDistance.config(text="calculating...")
        self.update()
        evtDispatcher.dispatch(EvtIds.EVT_INFORM_CALC_DISTANCE, {"row1": self.firstPosRow, "col1": self.firstPosCol,
                                                                 "row2": content["row"], "col2": content["col"],
                                                                 "isCriticalShortest": self.isCriticalShortest.get()})

    def handle_shortest_distance_calculated(self, content):
        if content is None or content["distance"] is None: return
        if content["distance"] == UNREACH_DISTANCE:
            self.lblDistance.config(text="UNREACHABLE")
            return
        res = "Shortest Distance: %d" % content["distance"]
        if not self.isCriticalShortest.get():
            res = "Possible Shortest Distance: %d" % content["distance"]
        self.lblDistance.config(text=res)
    
    def on_calc_distance_mode_clicked(self):
        if not self.isCalcDistanceMode.get():
            self.clean()
            self.cbCriticalShortest.deselect()
        evtDispatcher.dispatch(EvtIds.EVT_SET_CALC_DISTANCE_MODE, {"mode": self.isCalcDistanceMode.get()})

    def clean(self):
        self.lblStartPos.config(text="")
        self.lblEndPos.config(text="")
        self.lblDistance.config(text="")

