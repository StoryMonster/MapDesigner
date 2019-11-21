import os
from tkinter import Menu, messagebox

APP_VERSION = "v1.0.2019.1121"
CONTACTOR = "storymonster@aliyun.com"

class AboutSubmenu(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent, tearoff=0, bd=5)
        self.add_command(label="about product", command=self.about_product)
    
    def about_product(self):
        messagebox.showinfo("Msg Designer", "vesion: %s\ncontactor: %s" % (APP_VERSION, CONTACTOR))
