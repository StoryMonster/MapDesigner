import math
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
from model.data_parser import MapData, DataParser
from model.constances import EMPTY_NUMBER, LINE_GRID_TAG, BACK_GROUND_IMAGE_TAG, INVALID_COL, INVALID_ROW, PATH_TAG, UNREACH_DISTANCE
from model.path_calculator import PathCalculator, MapPath
from io import BytesIO
from copy import deepcopy
from event.event_dispatcher import evtDispatcher
from event.event_ids import EvtIds

class DisplayCanvas(Canvas):
    def __init__(self, parent, width, height):
        self.width, self.height = width, height
        Canvas.__init__(self, parent, width=self.width, height=self.height)
        self.parent = parent
        self.bgImg = None
        self.widthPerGrid = 0
        self.heightPerGrid = 0
        self.row = 0
        self.col = 0
        self.imgBytes = []
        self.gridWeights = []
        self.num = EMPTY_NUMBER
        self.isCalcDistanceMode = False
        self.isFirstPosSelected = False
        self.bind("<Button-1>", self.on_grid_clicked)
        self.bind("<Button-3>", self.on_erase_grid)
        self.bind("<B1-Motion>", self.on_grid_clicked)
        evtDispatcher.register(EvtIds.EVT_SET_CALC_DISTANCE_MODE, self.handle_mode_change)
        evtDispatcher.register(EvtIds.EVT_INFORM_TO_DRAW_GRIDS, self.handle_draw_grids)
        evtDispatcher.register(EvtIds.EVT_INFORM_GET_MAP_DATA, self.handle_get_map_data)
        evtDispatcher.register(EvtIds.EVT_INFORM_SAVE_PROJECT, self.handle_save_project)
        evtDispatcher.register(EvtIds.EVT_INFORM_NUMBER_CHANGED, self.handle_number_changed)
        evtDispatcher.register(EvtIds.EVT_INFORM_LOAD_PICTURE, self.handle_load_image)
        evtDispatcher.register(EvtIds.EVT_INFORM_CLEAR_NUMBERS, self.handle_clear_numbers)
        evtDispatcher.register(EvtIds.EVT_INFORM_CLEAR_PATH, self.handle_clear_path)
        evtDispatcher.register(EvtIds.EVT_INFORM_CALC_DISTANCE, self.handle_calc_distance)

    def handle_mode_change(self, content):
        if content is None or content["mode"] is None: return
        self.isCalcDistanceMode = content["mode"]
        if not self.isCalcDistanceMode:
            self.clear_path()

    def handle_draw_grids(self, content):
        if content is None or content["row"] is None or content["col"] is None: return
        self.draw_grid(content["row"], content["col"])
        evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": True})

    def handle_get_map_data(self, content):
        if content is None or content["mapdata"] is None or not isinstance(content["mapdata"], MapData): return
        self.apply_map_data(content["mapdata"])

    def handle_save_project(self, content):
        if content is None or content["filepath"] is None: return
        mapData = MapData(self.row, self.col, deepcopy(self.gridWeights),  deepcopy(self.imgBytes))
        messagebox.showinfo("info", f"len = {len(self.imgBytes)}")
        DataParser().save_to_file(content["filepath"], mapData)
        evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": False})

    def handle_number_changed(self, content):
        if content is None or content["number"] is None: return
        self.num = content["number"]

    def handle_load_image(self, content):
        if content is None or content["imgpath"] is None: return
        self.clear_all_numbers()
        self.clear_path()
        self.clear_grid_lines()
        self.show_background_image(content["imgpath"])
        self.row, self.col = 0, 0
        self.gridWeights = []
        evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": True})

    def handle_clear_numbers(self, content):
        self.clear_all_numbers()
        self.gridWeights = [EMPTY_NUMBER for _ in range(self.row * self.col)]
        evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": True})

    def handle_clear_path(self, content):
        self.clear_path()

    def handle_calc_distance(self, content):
        if (content is None or content["row1"] is None or content["col1"] is None or
            content["row2"] is None or content["col2"] is None or content["isCriticalShortest"] is None): return
        mapPath = None
        if content["isCriticalShortest"]:
            mapPath = PathCalculator(self.gridWeights, self.row, self.col).get_the_shortest_path(content["row1"], content["col1"], content["row2"], content["col2"])
        else:
            mapPath = PathCalculator(self.gridWeights, self.row, self.col).get_maybe_shortest_path(content["row1"], content["col1"], content["row2"], content["col2"])
        if mapPath is not None:
            self.draw_path_nodes(mapPath.nodes)
        evtDispatcher.dispatch(EvtIds.EVT_SHORTEST_DISTANCE_CALCULATED, {"distance": mapPath.distance if mapPath is not None else UNREACH_DISTANCE})

    def show_background_image(self, pic):
        self.delete(BACK_GROUND_IMAGE_TAG)
        with open(pic, "rb") as fd:
            self.imgBytes = fd.read()
        fd = Image.open(pic)
        img = fd.resize((self.width, self.height), Image.ANTIALIAS)
        self.bgImg = ImageTk.PhotoImage(img)
        self.create_image(0, 0, image=self.bgImg, anchor="nw", tag=BACK_GROUND_IMAGE_TAG)
    
    def show_background_image_from_bytes(self, data):
        self.delete(BACK_GROUND_IMAGE_TAG)
        if len(data) == 0:
            self.bgImg = None
            return
        self.imgBytes = data
        fd = Image.open(BytesIO(data))
        img = fd.resize((self.width, self.height), Image.ANTIALIAS)
        self.bgImg = ImageTk.PhotoImage(img)
        self.create_image(0, 0, image=self.bgImg, anchor="nw", tag=BACK_GROUND_IMAGE_TAG)

    def draw_grid(self, row, col):
        if self.bgImg is None:
            messagebox.showerror("Error", "No pictual is loaded!")
            return
        if row <= 0 or col <= 0:
            messagebox.showerror("Error", "Row and Col should all be positive integers")
            return

        self.clear_grid_lines()
        self.clear_all_numbers()
        self.row, self.col = row, col
        self.gridWeights = [EMPTY_NUMBER for _ in range(self.row * self.col)]
        self.widthPerGrid = self.width / self.col
        self.heightPerGrid = self.height / self.row
        for i in range(self.row):
            self.create_line(0, i*self.heightPerGrid, self.width, i*self.heightPerGrid, tag=LINE_GRID_TAG)
        for i in range(self.col):
            self.create_line(i*self.widthPerGrid, 0, i*self.widthPerGrid, self.height, tag=LINE_GRID_TAG)

    def clear_all_numbers(self):
        for i in range(self.row):
            for j in range(self.col):
                self.delete("num(%d,%d)" % (i, j))

    def clear_grid_lines(self):
        self.delete(LINE_GRID_TAG)

    def put_number_in_grid(self, num, row, col):
        offset = int(row * self.col + col)
        if offset >= len(self.gridWeights): return False
        if self.gridWeights[offset] == num: return False
        self.delete("num(%d,%d)" % (row, col))
        y = row * self.heightPerGrid + self.heightPerGrid / 2
        x = col * self.widthPerGrid + self.widthPerGrid / 2
        strNum = ""
        flags = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']
        if num < len(flags):
            strNum = flags[num]
        self.gridWeights[offset] = num
        self.create_text((x, y), text=strNum, fill="green", tag="num(%d,%d)" % (row, col))
        return True

    def on_grid_clicked(self, event):
        if not self.is_click_enabled(): return
        col = math.floor(event.x/self.widthPerGrid)
        row = math.floor(event.y/self.heightPerGrid)
        if self.isCalcDistanceMode:
            y = row * self.heightPerGrid + self.heightPerGrid / 2
            x = col * self.widthPerGrid + self.widthPerGrid / 2
            if not self.isFirstPosSelected:
                self.clear_path()
                self.create_text((x, y), text='@', fill="red", tag=PATH_TAG)
                evtDispatcher.dispatch(EvtIds.EVT_FIRST_POSITION_SELECTED, {"row": row, "col": col})
                self.isFirstPosSelected = True
                return
            self.isFirstPosSelected = False
            self.create_text((x, y), text='@', fill="red", tag=PATH_TAG)
            evtDispatcher.dispatch(EvtIds.EVT_SECOND_POSITION_SELECTED, {"row": row, "col": col})
        elif self.put_number_in_grid(self.num, row, col):
            evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": True})

    def on_erase_grid(self, event):
        if not self.is_click_enabled(): return
        if self.isCalcDistanceMode:
            pass
        else:
            row, col = math.floor(event.y/self.heightPerGrid), math.floor(event.x/self.widthPerGrid)
            offset = int(row * self.col + col)
            if offset >= len(self.gridWeights) or self.gridWeights[offset] == EMPTY_NUMBER: return
            self.delete("num(%d,%d)" % (row, col))
            evtDispatcher.dispatch(EvtIds.EVT_CONTENT_CHANGED, {"isChanged": True})

    def is_click_enabled(self):
        return self.bgImg != None and self.widthPerGrid > 0 and self.heightPerGrid > 0

    def extract_map_data(self):
        return MapData(self.row, self.col, deepcopy(self.gridWeights),  deepcopy(self.imgBytes))

    def draw_path_nodes(self, nodes):
        for i in range(len(nodes)):
            if i == len(nodes)-1: continue
            y1 = nodes[i][0] * self.heightPerGrid + self.heightPerGrid / 2
            x1 = nodes[i][1] * self.widthPerGrid + self.widthPerGrid / 2
            y2 = nodes[i+1][0] * self.heightPerGrid + self.heightPerGrid / 2
            x2 = nodes[i+1][1] * self.widthPerGrid + self.widthPerGrid / 2
            self.create_line(x1, y1, x2, y2, fill="red", tag=PATH_TAG)

    def clear_path(self):
        self.delete(PATH_TAG)

    def apply_map_data(self, mapdata):
        self.gridWeights = deepcopy(mapdata.gridWeights)
        self.show_background_image_from_bytes(deepcopy(mapdata.imgData))
        if mapdata.row > 0 and mapdata.col > 0:
            self.draw_grid(mapdata.row, mapdata.col)
        row, col = 0, 0
        for val in mapdata.gridWeights:
            self.put_number_in_grid(val, row, col)
            col += 1
            if col == self.col:
                col = 0
                row += 1
