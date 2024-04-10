import tkinter as tk
from frames.MainFrame import MainFrame

DEFAULT_WINDOW_WIDTH = 300
DEFAULT_WINDOW_HEIGHT = 200
DEFAULT_TITLE = "Security Application - Artur Śpiewak & Przemysław Szumczyk"

class AppController(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(DEFAULT_TITLE)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")
        
        # Initialize the main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (MainFrame,):
            frame_name = F.__name__
            frame = F(parent=container)
            self.frames[frame_name] = frame

            # Put all of the frames in the same location;
            # The one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainFrame")

    def show_frame(self, frame_name):
        '''Show a frame for the given frame name'''
        frame = self.frames[frame_name]
        frame.tkraise()