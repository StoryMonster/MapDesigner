from tkinter import Menu
from .submenu_file import FileSubmenu
from .submenu_about import AboutSubmenu

class MainMenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.filemenu = FileSubmenu(self)
        self.aboutmenu = AboutSubmenu(self)
        self.add_cascade(label="file", menu=self.filemenu)
        self.add_cascade(label="about", menu=self.aboutmenu)

        