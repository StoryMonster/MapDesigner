import math
from tkinter import Canvas, messagebox
from PIL import Image, ImageTk
from data_parser import MapData
from constances import EMPTY_NUMBER, LINE_GRID_TAG, BACK_GROUND_IMAGE_TAG, INVALID_COL, INVALID_ROW, PATH_TAG, UNREACH_DISTANCE
from io import BytesIO
from copy import deepcopy
from path_calculator import PathCalculator, MapPath

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
        self.bind("<Button-1>", self.on_grid_clicked)
        self.bind("<Button-3>", self.on_erase_grid)
        self.bind("<B1-Motion>", self.on_grid_clicked)
        self.start_row, self.start_col = INVALID_ROW, INVALID_COL   # is used to calculate the distance
        self.end_row, self.end_col = INVALID_ROW, INVALID_COL       # is used to calculate the distance

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
        if row <= 0 or col <= 0 or self.bgImg == None:
            messagebox.showerror("Error", f"Row{row} and Col{col} should be positive integer")
            return
        self.delete(LINE_GRID_TAG)
        self.widthPerGrid = self.width / row
        self.heightPerGrid = self.height / col
        self.row, self.col = 0, 0
        self.clear_all_marked_grids()
        self.row = row
        self.col = col
        self.gridWeights = [EMPTY_NUMBER for _ in range(row * col)]
        for i in range(row):
            self.create_line(0, i*self.heightPerGrid, self.width, i*self.heightPerGrid, tag=LINE_GRID_TAG)
        for i in range(col):
            self.create_line(i*self.widthPerGrid, 0, i*self.widthPerGrid, self.height, tag=LINE_GRID_TAG)
    
    def clear_all_marked_grids(self):
        self.gridWeights = [EMPTY_NUMBER for _ in range(self.row * self.col)]
        for i in range(self.row):
            for j in range(self.col):
                self.delete("num(%d,%d)" % (i, j))

    def set_number(self, num, row, col):
        offset = int(row * self.col + col)
        if offset >= len(self.gridWeights):
            return
        self.delete("num(%d,%d)" % (row, col))
        y = row * self.heightPerGrid + self.heightPerGrid / 2
        x = col * self.widthPerGrid + self.widthPerGrid / 2
        strNum = ""
        if num < 10 and num >=0: strNum = "%d" % num
        elif num == 10: strNum = "*"
        elif num == 11: strNum = "#"
        else: strNum = ""
        self.gridWeights[offset] = num
        self.create_text((x, y), text=strNum, fill="green", tag="num(%d,%d)" % (row, col))
    
    def on_grid_clicked(self, event):
        if not self.is_click_enabled(): return
        col = math.floor(event.x/self.widthPerGrid)
        row = math.floor(event.y/self.heightPerGrid)
        if self.parent.is_calc_distance_mode():
            y = row * self.heightPerGrid + self.heightPerGrid / 2
            x = col * self.widthPerGrid + self.widthPerGrid / 2
            if self.start_row == INVALID_ROW and self.start_col == INVALID_COL:
                self.clear_path()
                self.start_row = row
                self.start_col = col
                self.create_text((x, y), text='@', fill="red", tag=PATH_TAG)
                self.parent.show_start_position(self.start_col, self.start_row)
                return
            self.end_row = row
            self.end_col = col
            self.create_text((x, y), text='@', fill="red", tag=PATH_TAG)
            self.parent.show_end_position(self.end_col, self.end_row)
            mapPath = PathCalculator(self.gridWeights, self.row, self.col).get_the_shortest_path(self.start_row, self.start_col, self.end_row, self.end_col)
            self.start_row = INVALID_ROW
            self.start_col = INVALID_COL
            if mapPath is None:
                self.parent.show_distance(UNREACH_DISTANCE)
                return
            self.parent.show_distance(mapPath.distance)
            self.draw_path_nodes(mapPath.nodes)
        else:
            num = self.parent.get_selected_number()
            self.set_number(num, row, col)
    
    def on_erase_grid(self, event):
        if not self.is_click_enabled(): return
        if self.parent.is_calc_distance_mode():
            pass
        else:
            row, col = math.floor(event.y/self.heightPerGrid), math.floor(event.x/self.widthPerGrid)
            self.delete("num(%d,%d)" % (row, col))
    
    def is_click_enabled(self):
        return self.bgImg != None and self.widthPerGrid > 0 and self.heightPerGrid > 0
    
    def extract_map_data(self):
        return MapData(self.row, self.col, deepcopy(self.gridWeights),  deepcopy(self.imgBytes))

    def apply_map_data(self, mapdata):
        self.gridWeights = deepcopy(mapdata.gridWeights)
        self.show_background_image_from_bytes(mapdata.imgData)
        if mapdata.row > 0 and mapdata.col > 0:
            self.draw_grid(mapdata.row, mapdata.col)
        row, col = 0, 0
        for val in mapdata.gridWeights:
            self.set_number(val, row, col)
            col += 1
            if col == self.col:
                col = 0
                row += 1
    
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
