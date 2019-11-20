from tkinter import Tk, messagebox
from control_panel import ControlPanel
from display_panel import DisplayCanvas
from data_parser import MapData, DataParser
from menu import MainMenu

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Map Designer")
        self.canvas = DisplayCanvas(self, 700, 700)
        self.canvas.grid(row=0, column=0)
        self.ctrlPanel = ControlPanel(self)
        self.ctrlPanel.grid(row=0, column=1)
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.config(menu=MainMenu(self))
        self.projectPath = ""
        self.dataParser = DataParser()
    
    def draw_grids(self, row, col):
        self.canvas.draw_grid(row, col)
    
    def show_backgroud_picture(self, imgPath):
        self.canvas.show_background_image(imgPath)
    
    def clear_all_marked_grids(self):
        self.canvas.clear_all_marked_grids()
    
    def get_selected_number(self):
        return self.ctrlPanel.get_selected_number()
    
    def set_project_path(self, path):
        self.projectPath = path
        self.title(self.projectPath)

    def get_project_path(self):
        return self.projectPath
    
    def save_project(self):
        mapdata = self.canvas.extract_map_data()
        self.dataParser.save_to_file(self.projectPath, mapdata)
    
    def read_project(self, filepath):
        mapdata = self.dataParser.parse_from_file(filepath)
        if mapdata is not None:
            self.canvas.apply_map_data(mapdata)
            self.set_project_path(filepath)

    def is_calc_distance_mode(self):
        return self.ctrlPanel.is_calc_distance_mode()

    def show_start_position(self, x, y):
        self.ctrlPanel.show_start_position(x, y)

    def show_end_position(self, x, y):
        self.ctrlPanel.show_end_position(x, y)
    
    def show_distance(self, distance):
        self.ctrlPanel.show_distance(distance)

    def clear_path_grids(self):
        self.canvas.clear_path()

    def active_all_control_buttons(self):
        self.ctrlPanel.active_buttons()
